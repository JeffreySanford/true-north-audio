import { Controller, Post, Get, Body, Param, HttpException, HttpStatus } from '@nestjs/common';
import { MusicChatService } from './music-chat.service';

export class ChatMessageDto {
  message!: string;
  sessionId?: string;
  includeSuggestions?: boolean;
}

export class GenerateLyricsDto {
  theme!: string;
  style?: string;
  sessionId?: string;
}

export class GenerateFromChatDto {
  sessionId!: string;
  overrideParams?: Record<string, any>;
}

@Controller('api/music-chat')
export class MusicChatController {
  constructor(private readonly musicChatService: MusicChatService) {}

  /**
   * POST /api/music-chat/message
   * Send a message to the music assistant and get response with suggestions
   */
  @Post('message')
  async sendMessage(@Body() dto: ChatMessageDto) {
    try {
      const result = await this.musicChatService.chat(
        dto.message,
        dto.sessionId,
        dto.includeSuggestions !== false
      );
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      throw new HttpException(
        {
          success: false,
          message: 'Failed to process chat message',
          error: message,
        },
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * POST /api/music-chat/generate-lyrics
   * Generate lyrics based on theme
   */
  @Post('generate-lyrics')
  async generateLyrics(@Body() dto: GenerateLyricsDto) {
    try {
      const result = await this.musicChatService.generateLyrics(
        dto.theme,
        dto.style || 'country',
        dto.sessionId
      );
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      throw new HttpException(
        {
          success: false,
          message: 'Failed to generate lyrics',
          error: message,
        },
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * POST /api/music-chat/generate
   * Generate music from conversation session
   */
  @Post('generate')
  async generateFromChat(@Body() dto: GenerateFromChatDto) {
    try {
      const result = await this.musicChatService.generateFromConversation(
        dto.sessionId,
        dto.overrideParams
      );
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      throw new HttpException(
        {
          success: false,
          message: 'Failed to generate music from conversation',
          error: message,
        },
        HttpStatus.INTERNAL_SERVER_ERROR
      );
    }
  }

  /**
   * GET /api/music-chat/session/:id
   * Get session summary
   */
  @Get('session/:id')
  async getSession(@Param('id') sessionId: string) {
    try {
      const result = await this.musicChatService.getSessionSummary(sessionId);
      return result;
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      throw new HttpException(
        {
          success: false,
          message: 'Failed to retrieve session',
          error: message,
        },
        HttpStatus.NOT_FOUND
      );
    }
  }

  /**
   * GET /api/music-chat/health
   * Check if chat service is available
   */
  @Get('health')
  async healthCheck() {
    try {
      const health = await this.musicChatService.checkHealth();
      return {
        success: true,
        service: 'music-chat',
        ...health
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      throw new HttpException(
        {
          success: false,
          message: 'Chat service unavailable',
          error: message,
        },
        HttpStatus.SERVICE_UNAVAILABLE
      );
    }
  }
}
