import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { AudioAssetService } from './audio-asset.service';
import { AudioAsset } from '../models/audio-asset.model';


/**
 * Controller for audio asset management endpoints.
 * Provides REST API for CRUD operations on audio assets.
 */
@Controller('audio-assets')
export class AudioAssetController {
  /**
   * Injects AudioAssetService for asset management.
   * @param audioAssetService AudioAssetService instance
   */
  constructor(private readonly audioAssetService: AudioAssetService) {}

  /**
   * POST /audio-assets
   * Create a new audio asset.
   * @param data Partial audio asset data
   * @returns Observable emitting the created asset
   */
  @Post()
  create(@Body() data: Partial<AudioAsset>) {
    return this.audioAssetService.create(data);
  }

  /**
   * GET /audio-assets
   * Retrieve all audio assets.
   * @returns Observable emitting array of assets
   */
  @Get()
  findAll() {
    return this.audioAssetService.findAll();
  }

  /**
   * GET /audio-assets/:id
   * Retrieve an audio asset by ID.
   * @param id Asset ID
   * @returns Observable emitting the found asset or null
   */
  @Get(':id')
  findById(@Param('id') id: string) {
    return this.audioAssetService.findById(id);
  }

  /**
   * PUT /audio-assets/:id
   * Update an audio asset by ID.
   * @param id Asset ID
   * @param data Partial asset data
   * @returns Observable emitting the updated asset or null
   */
  @Put(':id')
  update(@Param('id') id: string, @Body() data: Partial<AudioAsset>) {
    return this.audioAssetService.update(id, data);
  }

  /**
   * DELETE /audio-assets/:id
   * Delete an audio asset by ID.
   * @param id Asset ID
   * @returns Observable emitting the deleted asset or null
   */
  @Delete(':id')
  delete(@Param('id') id: string) {
    return this.audioAssetService.delete(id);
  }
}
