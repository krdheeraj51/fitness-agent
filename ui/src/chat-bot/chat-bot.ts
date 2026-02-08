import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatBotService } from '../services/chat.bot.service';

interface Message {
  text: string;
  sender: 'user' | 'agent';
  loading?: boolean;
}

@Component({
  selector: 'app-chat-bot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chat-bot.html',
  styleUrls: ['./chat-bot.css']
})
export class ChatBot {
  prompt: string = '';
  messages: Message[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(private agentService: ChatBotService) { }

  sendPrompt(): void {
    const trimmedPrompt = this.prompt.trim();

    if (!trimmedPrompt) {
      this.errorMessage = 'Please enter a question!';
      return;
    }

    // Clear error and add user message
    this.errorMessage = '';
    this.messages.push({ text: trimmedPrompt, sender: 'user' });

    // Clear input and show loading
    this.prompt = '';
    this.isLoading = true;

    // Add loading message
    this.messages.push({ text: 'Thinking...', sender: 'agent', loading: true });

    // Call agent API using service
    this.agentService.sendPrompt(trimmedPrompt).subscribe({
      next: (response) => {
        // Remove loading message
        this.messages = this.messages.filter(m => !m.loading);

        if (response.status === 'success') {
          this.messages.push({ text: response.result, sender: 'agent' });
        } else {
          this.errorMessage = 'Error: ' + response.status;
        }
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error:', error);
        // Remove loading message
        this.messages = this.messages.filter(m => !m.loading);
        this.errorMessage = 'Failed to connect to agent. Make sure backend is running!';
        this.isLoading = false;
      }
    });
  }

  handleKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && event.ctrlKey) {
      this.sendPrompt();
    }
  }
}