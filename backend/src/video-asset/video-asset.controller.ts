import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { VideoAssetService } from './video-asset.service';
import { VideoAsset } from '../models/video-asset.model';

@Controller('video-assets')
export class VideoAssetController {
  constructor(private readonly videoAssetService: VideoAssetService) {}


  @Post()
  create(@Body() data: Partial<VideoAsset>) {
    return this.videoAssetService.create(data);
  }


  @Get()
  findAll() {
    return this.videoAssetService.findAll();
  }


  @Get(':id')
  findById(@Param('id') id: string) {
    return this.videoAssetService.findById(id);
  }


  @Put(':id')
  update(@Param('id') id: string, @Body() data: Partial<VideoAsset>) {
    return this.videoAssetService.update(id, data);
  }


  @Delete(':id')
  delete(@Param('id') id: string) {
    return this.videoAssetService.delete(id);
  }
}
