import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatBot } from '../chat-bot/chat-bot';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, ChatBot],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('ui');
}
