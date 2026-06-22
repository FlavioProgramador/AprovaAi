import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TopicAnalysis {
  id?: number;
  name: string;
  weight: string;
  relevance_percentage: number;
  study_recommendation: string;
  status?: string;
  questions_solved?: number;
  questions_correct?: number;
}

export interface AnalysisResponse {
  metadata: {
    edital_id?: number;
    extracted_topics_count: number;
    status?: string;
  };
  topics: TopicAnalysis[];
  general_strategy: string;
}

@Injectable({
  providedIn: 'root'
})
export class EditalService {
  private apiUrl = 'http://localhost:8000/api/v1/edital';

  constructor(private http: HttpClient) {}

  analyzeEdital(file: File): Observable<AnalysisResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/analyze`, formData);
  }

  getLatestEdital(): Observable<AnalysisResponse> {
    return this.http.get<AnalysisResponse>(`${this.apiUrl}/latest`);
  }

  updateTopic(topicId: number, data: { status: string; questions_solved: number; questions_correct: number }): Observable<TopicAnalysis> {
    return this.http.put<TopicAnalysis>(`${this.apiUrl}/topics/${topicId}`, data);
  }

  createStudySession(topicId: number, durationMinutes: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/topics/${topicId}/session`, {
      topic_id: topicId,
      duration_minutes: durationMinutes
    });
  }

  getHealth(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/health`);
  }
}
