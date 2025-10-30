import { Schema, Document, model, Types } from 'mongoose';

export interface AudioAsset extends Document {
  title: string;
  genre: Types.ObjectId;
  vocalFeatures: Types.ObjectId[];
  filePath: string;
}

const AudioAssetSchema = new Schema<AudioAsset>({
  title: { type: String, required: true },
  genre: { type: Schema.Types.ObjectId, ref: 'Genre', required: true },
  vocalFeatures: [{ type: Schema.Types.ObjectId, ref: 'VocalFeature' }],
  filePath: { type: String, required: true },
});

export const AudioAssetModel = model<AudioAsset>('AudioAsset', AudioAssetSchema);
