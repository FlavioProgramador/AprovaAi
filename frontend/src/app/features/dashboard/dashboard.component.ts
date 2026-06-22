import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EditalService, AnalysisResponse, TopicAnalysis } from '../../core/services/edital.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  selectedFile: File | null = null;
  analysisResult: AnalysisResponse | null = null;
  isLoading = false;
  errorMessage = '';

  constructor(private editalService: EditalService) {}

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
      next: (response) => {
        this.analysisResult = response;
        this.isLoading = false;
      },
      error: (err) => {
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

  reset(): void {
    this.selectedFile = null;
    this.analysisResult = null;
    this.errorMessage = '';
  }
}
