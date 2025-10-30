import { Test, TestingModule } from '@nestjs/testing';
import { getModelToken } from '@nestjs/mongoose';
import { AudioAssetService } from './audio-asset.service';

const mockAudioAssetModel = {
  create: jest.fn(),
  find: jest.fn().mockReturnThis(),
  exec: jest.fn(),
  findById: jest.fn().mockReturnThis(),
  findByIdAndUpdate: jest.fn().mockReturnThis(),
  findByIdAndDelete: jest.fn().mockReturnThis(),
};


/**
 * Unit tests for AudioAssetService.
 * Verifies CRUD operations and model integration.
 */
describe('AudioAssetService', () => {
  let service: AudioAssetService;
  let model: typeof mockAudioAssetModel;

  /**
   * Setup test module with mocked AudioAsset model.
   */
  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AudioAssetService,
        { provide: getModelToken('AudioAsset'), useValue: mockAudioAssetModel },
      ],
    }).compile();

    service = module.get<AudioAssetService>(AudioAssetService);
    model = module.get(getModelToken('AudioAsset'));
  });

  /**
   * Should create an audio asset.
   */
  it('should create an audio asset', async () => {
    model.create.mockResolvedValue({ title: 'Song' });
    const result = await service.create({ title: 'Song' });
    expect(result).toEqual({ title: 'Song' });
    expect(model.create).toHaveBeenCalledWith({ title: 'Song' });
  });

  /**
   * Should find all audio assets.
   */
  it('should find all audio assets', async () => {
    model.find.mockReturnValue({ populate: () => ({ populate: () => ({ exec: () => Promise.resolve([{ title: 'Track' }]) }) }) });
    const result = await service.findAll();
    expect(result).toEqual([{ title: 'Track' }]);
  });

  /**
   * Should find an audio asset by id.
   */
  it('should find an audio asset by id', async () => {
    model.findById.mockReturnValue({ populate: () => ({ populate: () => ({ exec: () => Promise.resolve({ title: 'Track' }) }) }) });
    const result = await service.findById('123');
    expect(result).toEqual({ title: 'Track' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  /**
   * Should update an audio asset.
   */
  it('should update an audio asset', async () => {
    model.findByIdAndUpdate.mockReturnValue({ exec: () => Promise.resolve({ title: 'Updated' }) });
    const result = await service.update('123', { title: 'Updated' });
    expect(result).toEqual({ title: 'Updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { title: 'Updated' }, { new: true });
  });

  /**
   * Should delete an audio asset.
   */
  it('should delete an audio asset', async () => {
    model.findByIdAndDelete.mockReturnValue({ exec: () => Promise.resolve({ title: 'Deleted' }) });
    const result = await service.delete('123');
    expect(result).toEqual({ title: 'Deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
