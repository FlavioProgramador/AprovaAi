import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface TopicAnalysis {
  name: string;
  weight: string;
  relevance_percentage: number;
  study_recommendation: string;
}

export interface AnalysisResponse {
  metadata: {
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

  getHealth(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/health`);
  }
}
