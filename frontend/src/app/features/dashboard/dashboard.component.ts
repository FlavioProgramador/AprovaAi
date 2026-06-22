import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { EditalService, AnalysisResponse, TopicAnalysis } from '../../core/services/edital.service';
import { AuthService } from '../../core/services/auth.service';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit, AfterViewInit {
  @ViewChild('radarCanvas') radarCanvas!: ElementRef;
  
  selectedFile: File | null = null;
  analysisResult: AnalysisResponse | null = null;
  isLoading = false;
  errorMessage = '';
  userEmail = '';

  // Chart
  chartInstance: Chart | null = null;

  // Pomodoro
  pomodoroMinutes = 25;
  pomodoroSeconds = 0;
  pomodoroActive = false;
  pomodoroTimerId: any = null;
  pomodoroSelectedTopic: TopicAnalysis | null = null;
  pomodoroDuration = 25; // 25 or 50
  pomodoroCompletedCount = 0;

  constructor(
    private editalService: EditalService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      if (user) {
        this.userEmail = user.email;
      }
    });

    this.loadLatestEdital();
  }

  ngAfterViewInit(): void {
    if (this.analysisResult) {
      setTimeout(() => this.renderChart(this.analysisResult!.topics), 150);
    }
  }

  loadLatestEdital(): void {
    this.isLoading = true;
    this.editalService.getLatestEdital().subscribe({
      next: (response) => {
        this.analysisResult = response;
        this.isLoading = false;
        if (response.topics && response.topics.length > 0) {
          this.pomodoroSelectedTopic = response.topics[0];
        }
        setTimeout(() => this.renderChart(response.topics), 150);
      },
      error: (err) => {
        this.isLoading = false;
        console.log('Nenhum edital anterior encontrado para carregar automaticamente.');
      }
    });
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      this.selectedFile = file;
      this.errorMessage = '';
    } else {
      this.selectedFile = null;
      this.errorMessage = 'Por favor, selecione apenas arquivos PDF.';
    }
  }

  uploadAndAnalyze(): void {
    if (!this.selectedFile) return;

    this.isLoading = true;
    this.errorMessage = '';
    this.analysisResult = null;

    this.editalService.analyzeEdital(this.selectedFile).subscribe({
      next: (response: AnalysisResponse) => {
        this.analysisResult = response;
        this.isLoading = false;
        if (response.topics && response.topics.length > 0) {
          this.pomodoroSelectedTopic = response.topics[0];
        }
        setTimeout(() => this.renderChart(response.topics), 150);
      },
      error: (err: any) => {
        console.error(err);
        this.isLoading = false;
        this.errorMessage = err.error?.detail || 'Ocorreu um erro ao analisar o edital. Verifique se o servidor backend está ativo.';
      }
    });
  }

  getWeightClass(weight: string): string {
    switch (weight.toLowerCase()) {
      case 'alto':
        return 'bg-red-500/10 text-red-400 border border-red-500/20';
      case 'médio':
      case 'medio':
        return 'bg-amber-500/10 text-amber-400 border border-amber-500/20';
      case 'baixo':
      default:
        return 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20';
    }
  }

  saveTopicProgress(topic: TopicAnalysis): void {
    if (!topic.id) return;
    
    const solved = Math.max(0, Number(topic.questions_solved) || 0);
    const correct = Math.max(0, Number(topic.questions_correct) || 0);
    const statusVal = topic.status || 'to_study';

    this.editalService.updateTopic(topic.id, {
      status: statusVal,
      questions_solved: solved,
      questions_correct: correct
    }).subscribe({
      next: (updatedTopic) => {
        topic.status = updatedTopic.status;
        topic.questions_solved = updatedTopic.questions_solved;
        topic.questions_correct = updatedTopic.questions_correct;
        
        if (this.analysisResult) {
          this.renderChart(this.analysisResult.topics);
        }
      },
      error: (err) => {
        console.error('Erro ao atualizar tópico:', err);
        alert('Erro ao salvar progresso do tópico.');
      }
    });
  }

  exportCSV(): void {
    if (!this.analysisResult || !this.analysisResult.metadata.edital_id) return;
    const editalId = this.analysisResult.metadata.edital_id;
    const token = this.authService.getToken();
    
    this.isLoading = true;
    fetch(`http://localhost:8000/api/v1/export/csv/${editalId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    .then(response => {
      if (!response.ok) throw new Error('Falha ao exportar');
      return response.blob();
    })
    .then(blob => {
      this.isLoading = false;
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `plano_de_estudos_${editalId}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    })
    .catch(err => {
      this.isLoading = false;
      console.error(err);
      alert('Erro ao exportar o plano de estudos.');
    });
  }

  selectTopicForPomodoro(topic: TopicAnalysis): void {
    this.pomodoroSelectedTopic = topic;
  }

  setPomodoroDuration(duration: number): void {
    this.pomodoroDuration = duration;
    this.resetPomodoro();
  }

  startPomodoro(): void {
    if (this.pomodoroActive) return;
    this.pomodoroActive = true;
    this.pomodoroTimerId = setInterval(() => this.tickPomodoro(), 1000);
  }

  pausePomodoro(): void {
    if (!this.pomodoroActive) return;
    this.pomodoroActive = false;
    if (this.pomodoroTimerId) {
      clearInterval(this.pomodoroTimerId);
    }
  }

  resetPomodoro(): void {
    this.pausePomodoro();
    this.pomodoroMinutes = this.pomodoroDuration;
    this.pomodoroSeconds = 0;
  }

  tickPomodoro(): void {
    if (this.pomodoroSeconds === 0) {
      if (this.pomodoroMinutes === 0) {
        this.finishPomodoro();
        return;
      }
      this.pomodoroMinutes--;
      this.pomodoroSeconds = 59;
    } else {
      this.pomodoroSeconds--;
    }
  }

  finishPomodoro(): void {
    this.pausePomodoro();
    this.playBeep();
    this.pomodoroCompletedCount++;
    
    if (this.pomodoroSelectedTopic && this.pomodoroSelectedTopic.id) {
      const topicId = this.pomodoroSelectedTopic.id;
      const duration = this.pomodoroDuration;
      
      this.editalService.createStudySession(topicId, duration).subscribe({
        next: () => {
          if (this.pomodoroSelectedTopic && this.pomodoroSelectedTopic.status === 'to_study') {
            this.pomodoroSelectedTopic.status = 'studying';
          }
          alert(`Parabéns! Sessão de ${duration} minutos salva para o assunto: ${this.pomodoroSelectedTopic?.name}`);
        },
        error: (err) => {
          console.error('Erro ao registrar sessão de estudos:', err);
        }
      });
    } else {
      alert(`Parabéns! Você concluiu um ciclo de estudos de ${this.pomodoroDuration} minutos.`);
    }
    
    this.resetPomodoro();
  }

  playBeep(): void {
    try {
      const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)();
      
      const playSingleBeep = (delay: number) => {
        setTimeout(() => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          
          osc.type = 'sine';
          osc.frequency.setValueAtTime(880, audioCtx.currentTime);
          gain.gain.setValueAtTime(0.35, audioCtx.currentTime);
          
          osc.start();
          gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
          
          setTimeout(() => {
            osc.stop();
          }, 350);
        }, delay);
      };

      playSingleBeep(0);
      playSingleBeep(450);
      playSingleBeep(900);
    } catch (e) {
      console.error('Falha ao inicializar áudio nativo:', e);
    }
  }

  renderChart(topics: TopicAnalysis[]): void {
    if (!this.radarCanvas) return;

    if (this.chartInstance) {
      this.chartInstance.destroy();
    }

    const sortedTopics = [...topics]
      .sort((a, b) => b.relevance_percentage - a.relevance_percentage)
      .slice(0, 6);

    const labels = sortedTopics.map(t => {
      return t.name.length > 22 ? t.name.substring(0, 19) + '...' : t.name;
    });
    
    const relevanceData = sortedTopics.map(t => t.relevance_percentage);
    
    const weightMap: Record<string, number> = { 'alto': 90, 'médio': 60, 'medio': 60, 'baixo': 30 };
    const weightData = sortedTopics.map(t => weightMap[t.weight.toLowerCase()] || 30);

    const ctx = this.radarCanvas.nativeElement.getContext('2d');
    
    this.chartInstance = new Chart(ctx, {
      type: 'radar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Relevância da Matéria (%)',
            data: relevanceData,
            fill: true,
            backgroundColor: 'rgba(56, 189, 248, 0.25)',
            borderColor: 'rgba(56, 189, 248, 0.85)',
            pointBackgroundColor: '#38bdf8',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(56, 189, 248, 1)'
          },
          {
            label: 'Prioridade Sugerida (10-100)',
            data: weightData,
            fill: true,
            backgroundColor: 'rgba(192, 132, 252, 0.2)',
            borderColor: 'rgba(192, 132, 252, 0.85)',
            pointBackgroundColor: '#c084fc',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(192, 132, 252, 1)'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: '#94a3b8',
              font: {
                family: 'Inter',
                size: 11
              }
            }
          }
        },
        scales: {
          r: {
            angleLines: {
              color: '#222d45'
            },
            grid: {
              color: '#222d45'
            },
            pointLabels: {
              color: '#94a3b8',
              font: {
                family: 'Inter',
                size: 10,
                weight: 'bold'
              }
            },
            ticks: {
              backdropColor: 'transparent',
              color: '#64748b',
              font: {
                size: 8
              }
            },
            suggestedMin: 0,
            suggestedMax: 100
          }
        }
      }
    });
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  reset(): void {
    this.selectedFile = null;
    this.analysisResult = null;
    this.errorMessage = '';
    if (this.chartInstance) {
      this.chartInstance.destroy();
      this.chartInstance = null;
    }
  }
}
