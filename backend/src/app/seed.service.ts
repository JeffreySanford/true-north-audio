import { Injectable, OnModuleInit } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Genre } from '../models/genre.model';
import { AudioAsset } from '../models/audio-asset.model';

@Injectable()
export class SeedService implements OnModuleInit {
  constructor(
    @InjectModel('Genre') private readonly genreModel: Model<Genre>,
    @InjectModel('AudioAsset') private readonly audioAssetModel: Model<AudioAsset>
  ) {}

  async onModuleInit() {
    if (process.env.NODE_ENV !== 'production') {
      await this.seedGenres();
      await this.seedAudioAssets();
    }
  }

  async seedGenres() {
    const genres = [
      { name: 'Ambient', description: 'Atmospheric and relaxing' },
      { name: 'Rock', description: 'Energetic and guitar-driven' },
      { name: 'Pop', description: 'Catchy and mainstream' },
      { name: 'Jazz', description: 'Improvisational and smooth' }
    ];
    for (const genre of genres) {
      await this.genreModel.updateOne({ name: genre.name }, genre, { upsert: true });
    }
  }

  async seedAudioAssets() {
    // First, fetch all genres and build a name->ObjectId map
    const genres = await this.genreModel.find({});
  const genreMap = new Map<string, string>();
  genres.forEach((g) => genreMap.set(g.name, String(g._id)));

    const assets = [
      { title: 'Demo Track', genre: 'Ambient', filePath: '/assets/demo-track.mp3' },
      { title: 'Rock Anthem', genre: 'Rock', filePath: '/assets/rock-anthem.mp3' }
    ];
    for (const asset of assets) {
      const genreId = genreMap.get(asset.genre);
      if (!genreId) {
        console.warn(`[Seeding] Genre not found for asset: ${asset.title}, genre: ${asset.genre}`);
        continue;
      }
      await this.audioAssetModel.updateOne(
        { title: asset.title },
        { ...asset, genre: genreId },
        { upsert: true }
      );
    }
  }
}
