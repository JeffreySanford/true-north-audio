import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';

@Schema()
export class Instrument {
  @Prop({ required: true, unique: true })
  name!: string;
}

export type InstrumentDocument = Instrument & Document;
export const InstrumentSchema = SchemaFactory.createForClass(Instrument);
