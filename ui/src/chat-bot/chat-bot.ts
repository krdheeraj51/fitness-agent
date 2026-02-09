import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatBotService } from '../services/chat.bot.service';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

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

  constructor(private agentService: ChatBotService,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer
  ) { }

  formatMessage(text: string): SafeHtml {
    if (!text) return '';

    // Convert markdown-like formatting to HTML
    let formatted = text
      // Escape HTML first
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      // Bold text **text**
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      // Italic text *text*
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      // Line breaks
      .replace(/\n/g, '<br>')
      // Lists with dash
      .replace(/^- (.*)$/gm, '• $1');

    return this.sanitizer.bypassSecurityTrustHtml(formatted);
  }


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

        if (response.status === 'success' && response.response) {
          console.log('Agent response:', response.response);
          this.messages.push({ text: response.response, sender: 'agent' });
          console.log('Agent response added to messages');
          console.log('Current messages:', this.messages);
        } else {
          this.errorMessage = 'Error: ' + response.status;
        }
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('Error:', error);
        // Remove loading message
        this.messages = this.messages.filter(m => !m.loading);
        this.errorMessage = 'Failed to connect to agent. Make sure backend is running!';
        this.isLoading = false;
        this.cdr.detectChanges();
      }
    });
  }

  handleKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter' && event.ctrlKey) {
      this.sendPrompt();
    }
  }
}