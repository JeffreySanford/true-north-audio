import { Injectable, Logger } from '@nestjs/common';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class MusicChatService {
  private readonly logger = new Logger(MusicChatService.name);
  private readonly pythonApiUrl = process.env.PYTHON_API_URL || 'http://localhost:8000';

  constructor(private readonly httpService: HttpService) {}

  /**
   * Send chat message to Python music assistant
   */
  async chat(
    message: string,
    sessionId?: string,
    includeSuggestions: boolean = true
  ): Promise<any> {
    try {
      this.logger.log(`Chat message: "${message.substring(0, 50)}..."`);

      const response = await firstValueFrom(
        this.httpService.post(`${this.pythonApiUrl}/chat/message`, {
          message,
          session_id: sessionId,
          include_suggestions: includeSuggestions,
        })
      );

      return response.data;
    } catch (error) {
      this.logger.error('Chat service error:', error);
      throw error;
    }
  }

  /**
   * Generate lyrics using LLM
   */
  async generateLyrics(
    theme: string,
    style: string = 'country',
    sessionId?: string
  ): Promise<any> {
    try {
      this.logger.log(`Generating lyrics: theme="${theme}", style="${style}"`);

      const response = await firstValueFrom(
        this.httpService.post(`${this.pythonApiUrl}/chat/generate-lyrics`, {
          theme,
          style,
          session_id: sessionId,
        })
      );

      return response.data;
    } catch (error) {
      this.logger.error('Lyrics generation error:', error);
      throw error;
    }
  }

  /**
   * Generate music from conversation session
   */
  async generateFromConversation(
    sessionId: string,
    overrideParams?: Record<string, any>
  ): Promise<any> {
    try {
      this.logger.log(`Generating from conversation: session=${sessionId}`);

      const response = await firstValueFrom(
        this.httpService.post(`${this.pythonApiUrl}/chat/generate`, {
          session_id: sessionId,
          override_params: overrideParams,
        })
      );

      return response.data;
    } catch (error) {
      this.logger.error('Generation from chat error:', error);
      throw error;
    }
  }

  /**
   * Get session summary
   */
  async getSessionSummary(sessionId: string): Promise<any> {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.pythonApiUrl}/chat/session/${sessionId}`)
      );

      return response.data;
    } catch (error) {
      this.logger.error(`Session retrieval error: ${sessionId}`, error);
      throw error;
    }
  }

  /**
   * Check if chat service is healthy
   */
  async checkHealth(): Promise<any> {
    try {
      const response = await firstValueFrom(
        this.httpService.get(`${this.pythonApiUrl}/chat/health`, {
          timeout: 5000,
        })
      );

      return {
        available: true,
        ...response.data,
      };
    } catch (error) {
      this.logger.warn('Chat service health check failed:', error);
      return {
        available: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }
}
