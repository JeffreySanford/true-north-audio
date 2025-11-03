import { Controller, Get } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Instrument, InstrumentDocument } from './schemas/instrument.schema';

@Controller('api/instruments')
export class InstrumentController {
  constructor(
    @InjectModel(Instrument.name) private instrumentModel: Model<InstrumentDocument>
  ) {}

  @Get()
  async listInstruments(): Promise<string[]> {
    const instruments = await this.instrumentModel.find().lean();
    return instruments.map(i => i.name);
  }
}
