import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema()
export class Genre {
  @Prop({ required: true, unique: true })
  name!: string;

  @Prop()
  description!: string;

  @Prop()
  bpm!: number;

  @Prop()
  timeSignature!: string;

  @Prop()
  groove!: string;

  @Prop([String])
  instruments!: string[];

  @Prop([String])
  mandatoryInstruments!: string[];

  @Prop()
  scriptTemplate!: string;
}

export type GenreDocument = Genre & Document;
export const GenreSchema = SchemaFactory.createForClass(Genre);
