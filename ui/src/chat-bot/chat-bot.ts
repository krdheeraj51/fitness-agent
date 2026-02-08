import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatBotService } from '../services/chat.bot.service';

@Component({
  selector: 'app-chat-bot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-bot.html',
  styleUrls: ['./chat-bot.css'],
})
export class ChatBot {
  messages: { role: 'user' | 'assistant'; text: string }[] = [];
  input = '';
  loading = false;

  constructor(private chat: ChatBotService) { }

  async send() {
    const text = this.input.trim();
    if (!text) return;
    this.messages.push({ role: 'user', text });
    this.input = '';
    this.loading = true;
    try {
      const reply = await this.chat.sendPrompt(text);
      this.messages.push({ role: 'assistant', text: reply });
    } catch (e) {
      this.messages.push({ role: 'assistant', text: 'Error: ' + (e instanceof Error ? e.message : String(e)) });
    } finally {
      this.loading = false;
    }
  }
}
