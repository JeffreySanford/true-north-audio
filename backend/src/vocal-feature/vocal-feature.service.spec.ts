import { Test, TestingModule } from '@nestjs/testing';
import { getModelToken } from '@nestjs/mongoose';
import { VocalFeatureService } from './vocal-feature.service';

const mockVocalFeatureModel = {
  create: jest.fn(),
  find: jest.fn().mockReturnThis(),
  exec: jest.fn(),
  findById: jest.fn().mockReturnThis(),
  findByIdAndUpdate: jest.fn().mockReturnThis(),
  findByIdAndDelete: jest.fn().mockReturnThis(),
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
    model.create.mockResolvedValue({ name: 'Falsetto' });
    const result = await service.create({ name: 'Falsetto' });
    expect(result).toEqual({ name: 'Falsetto' });
    expect(model.create).toHaveBeenCalledWith({ name: 'Falsetto' });
  });

  it('should find all vocal features', async () => {
    model.find.mockReturnValue({ exec: () => Promise.resolve([{ name: 'Growl' }]) });
    const result = await service.findAll();
    expect(result).toEqual([{ name: 'Growl' }]);
  });

  it('should find a vocal feature by id', async () => {
    model.findById.mockReturnValue({ exec: () => Promise.resolve({ name: 'Scream' }) });
    const result = await service.findById('123');
    expect(result).toEqual({ name: 'Scream' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  it('should update a vocal feature', async () => {
    model.findByIdAndUpdate.mockReturnValue({ exec: () => Promise.resolve({ name: 'Updated' }) });
    const result = await service.update('123', { name: 'Updated' });
    expect(result).toEqual({ name: 'Updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { name: 'Updated' }, { new: true });
  });

  it('should delete a vocal feature', async () => {
    model.findByIdAndDelete.mockReturnValue({ exec: () => Promise.resolve({ name: 'Deleted' }) });
    const result = await service.delete('123');
    expect(result).toEqual({ name: 'Deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
