import { Schema, Document, model } from 'mongoose';

export interface Genre extends Document {
  name: string;
  description?: string;
}

const GenreSchema = new Schema<Genre>({
  name: { type: String, required: true, unique: true },
  description: { type: String },
});

export const GenreModel = model<Genre>('Genre', GenreSchema);
