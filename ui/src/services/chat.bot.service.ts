import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
// import { PromptRequest, AgentResponse } from '../../backend/main';

export interface PromptRequest {
  prompt: string;
}

export interface AgentResponse {
  result: string;
  status: string;
}
@Injectable({
  providedIn: 'root',
})
export class ChatBotService {
  // Sends the prompt to backend. Adjust URL as needed.

  private apiUrl = 'http://localhost:8000/agent/';

  constructor(private http: HttpClient) { }

  // sendPrompt(prompt: string): Observable<AgentResponse> {
  //   const request: PromptRequest = { prompt };
  //   return this.http.post<AgentResponse>(this.apiUrl, request);
  // }
  sendPrompt(prompt: string): Observable<AgentResponse> {
    const request: PromptRequest = { prompt };
    return this.http.post<AgentResponse>(this.apiUrl, request);
  }
}
