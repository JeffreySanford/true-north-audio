import { Test, TestingModule } from '@nestjs/testing';
import { lastValueFrom } from 'rxjs';
import { getModelToken } from '@nestjs/mongoose';
import { AudioAssetService } from './audio-asset.service';

const mockAudioAssetModel = {
  create: jest.fn(),
  find: jest.fn(),
  findById: jest.fn(),
  findByIdAndUpdate: jest.fn(),
  findByIdAndDelete: jest.fn(),
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
    model.create.mockReturnValue(Promise.resolve({ title: 'Song' }));
    const result = await lastValueFrom(service.create({ title: 'Song' }));
    expect(result).toEqual({ title: 'Song' });
    expect(model.create).toHaveBeenCalledWith({ title: 'Song' });
  });

  /**
   * Should find all audio assets.
   */
  it('should find all audio assets', async () => {
    model.find.mockReturnValue({
      populate: () => ({
        populate: () => ({
          exec: () => Promise.resolve([{ title: 'Track' }])
        })
      })
    });
    const result = await lastValueFrom(service.findAll());
    expect(result).toEqual([{ title: 'Track' }]);
  });

  /**
   * Should find an audio asset by id.
   */
  it('should find an audio asset by id', async () => {
    model.findById.mockReturnValue({
      populate: () => ({
        populate: () => ({
          exec: () => Promise.resolve({ title: 'Track' })
        })
      })
    });
    const result = await lastValueFrom(service.findById('123'));
    expect(result).toEqual({ title: 'Track' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  /**
   * Should update an audio asset.
   */
  it('should update an audio asset', async () => {
    model.findByIdAndUpdate.mockReturnValue({
      exec: () => Promise.resolve({ title: 'Updated' })
    });
    const result = await lastValueFrom(service.update('123', { title: 'Updated' }));
    expect(result).toEqual({ title: 'Updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { title: 'Updated' }, { new: true });
  });

  /**
   * Should delete an audio asset.
   */
  it('should delete an audio asset', async () => {
    model.findByIdAndDelete.mockReturnValue({
      exec: () => Promise.resolve({ title: 'Deleted' })
    });
    const result = await lastValueFrom(service.delete('123'));
    expect(result).toEqual({ title: 'Deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
