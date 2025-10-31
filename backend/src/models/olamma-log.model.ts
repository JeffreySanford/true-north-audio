import { Schema, Document, model } from 'mongoose';

export interface OlammaLog extends Document {
  prompt: string;
  audioUrl: string;
  createdAt: Date;
}

export const OlammaLogSchema = new Schema<OlammaLog>({
  prompt: { type: String, required: true },
  audioUrl: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
});

export const OlammaLogModel = model<OlammaLog>('OlammaLog', OlammaLogSchema);
