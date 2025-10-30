import { Schema, Document, model } from 'mongoose';

export interface VocalFeature extends Document {
  name: string;
  description?: string;
}

const VocalFeatureSchema = new Schema<VocalFeature>({
  name: { type: String, required: true, unique: true },
  description: { type: String },
});

export const VocalFeatureModel = model<VocalFeature>('VocalFeature', VocalFeatureSchema);
