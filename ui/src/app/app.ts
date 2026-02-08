import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ChatBot } from '../chat-bot/chat-bot';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ChatBot],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App {
  protected readonly title = signal('ui');
}
