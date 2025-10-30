import { Schema, Document, model } from 'mongoose';

export interface VideoAsset extends Document {
  title: string;
  filePath: string;
}

const VideoAssetSchema = new Schema<VideoAsset>({
  title: { type: String, required: true },
  filePath: { type: String, required: true },
});

export const VideoAssetModel = model<VideoAsset>('VideoAsset', VideoAssetSchema);
