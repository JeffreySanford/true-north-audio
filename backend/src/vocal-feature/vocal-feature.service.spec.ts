import { Test, TestingModule } from '@nestjs/testing';
import { lastValueFrom } from 'rxjs';
import { getModelToken } from '@nestjs/mongoose';
import { VocalFeatureService } from './vocal-feature.service';

const mockVocalFeatureModel = {
  create: jest.fn(),
  find: jest.fn(),
  findById: jest.fn(),
  findByIdAndUpdate: jest.fn(),
  findByIdAndDelete: jest.fn(),
};

describe('VocalFeatureService', () => {
  let service: VocalFeatureService;
  let model: typeof mockVocalFeatureModel;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        VocalFeatureService,
        { provide: getModelToken('VocalFeature'), useValue: mockVocalFeatureModel },
      ],
    }).compile();

    service = module.get<VocalFeatureService>(VocalFeatureService);
    model = module.get(getModelToken('VocalFeature'));
  });

  it('should create a vocal feature', async () => {
    model.create.mockReturnValue(Promise.resolve({ name: 'Falsetto' }));
    const result = await lastValueFrom(service.create({ name: 'Falsetto' }));
    expect(result).toEqual({ name: 'Falsetto' });
    expect(model.create).toHaveBeenCalledWith({ name: 'Falsetto' });
  });

  it('should find all vocal features', async () => {
    model.find.mockReturnValue({
      exec: () => Promise.resolve([{ name: 'Growl' }])
    });
    const result = await lastValueFrom(service.findAll());
    expect(result).toEqual([{ name: 'Growl' }]);
  });

  it('should find a vocal feature by id', async () => {
    model.findById.mockReturnValue({
      exec: () => Promise.resolve({ name: 'Scream' })
    });
    const result = await lastValueFrom(service.findById('123'));
    expect(result).toEqual({ name: 'Scream' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  it('should update a vocal feature', async () => {
    model.findByIdAndUpdate.mockReturnValue({
      exec: () => Promise.resolve({ name: 'Updated' })
    });
    const result = await lastValueFrom(service.update('123', { name: 'Updated' }));
    expect(result).toEqual({ name: 'Updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { name: 'Updated' }, { new: true });
  });

  it('should delete a vocal feature', async () => {
    model.findByIdAndDelete.mockReturnValue({
      exec: () => Promise.resolve({ name: 'Deleted' })
    });
    const result = await lastValueFrom(service.delete('123'));
    expect(result).toEqual({ name: 'Deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
