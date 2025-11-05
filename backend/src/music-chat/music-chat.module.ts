import { Module } from '@nestjs/common';
import { HttpModule } from '@nestjs/axios';
import { MusicChatController } from './music-chat.controller';
import { MusicChatService } from './music-chat.service';

@Module({
  imports: [
    HttpModule.register({
      timeout: 30000, // 30 second timeout for LLM responses
      maxRedirects: 5,
    }),
  ],
  controllers: [MusicChatController],
  providers: [MusicChatService],
  exports: [MusicChatService],
})
export class MusicChatModule {}
