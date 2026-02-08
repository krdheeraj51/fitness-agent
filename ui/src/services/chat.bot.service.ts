import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class ChatBotService {
  // Sends the prompt to backend. Adjust URL as needed.
  async sendPrompt(prompt: string): Promise<string> {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || res.statusText);
    }
    const data = await res.json();
    // expect backend shape: { reply: '...' }
    return data?.reply ?? data?.result ?? JSON.stringify(data);
  }
}
