import { Test, TestingModule } from '@nestjs/testing';
import { lastValueFrom } from 'rxjs';
import { getModelToken } from '@nestjs/mongoose';
import { VideoAssetService } from './video-asset.service';

const mockVideoAssetModel = {
  create: jest.fn(),
  find: jest.fn(),
  findById: jest.fn(),
  findByIdAndUpdate: jest.fn(),
  findByIdAndDelete: jest.fn(),
};

describe('VideoAssetService', () => {
  let service: VideoAssetService;
  let model: typeof mockVideoAssetModel;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        VideoAssetService,
        { provide: getModelToken('VideoAsset'), useValue: mockVideoAssetModel },
      ],
    }).compile();

    service = module.get<VideoAssetService>(VideoAssetService);
    model = module.get(getModelToken('VideoAsset'));
  });

  it('should create a video asset', async () => {
    model.create.mockReturnValue(Promise.resolve({ title: 'Video' }));
    const result = await lastValueFrom(service.create({ title: 'Video' }));
    expect(result).toEqual({ title: 'Video' });
    expect(model.create).toHaveBeenCalledWith({ title: 'Video' });
  });

  it('should find all video assets', async () => {
    model.find.mockReturnValue({
      exec: () => Promise.resolve([{ title: 'Clip' }])
    });
    const result = await lastValueFrom(service.findAll());
    expect(result).toEqual([{ title: 'Clip' }]);
  });

  it('should find a video asset by id', async () => {
    model.findById.mockReturnValue({
      exec: () => Promise.resolve({ title: 'Clip' })
    });
    const result = await lastValueFrom(service.findById('123'));
    expect(result).toEqual({ title: 'Clip' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  it('should update a video asset', async () => {
    model.findByIdAndUpdate.mockReturnValue({
      exec: () => Promise.resolve({ title: 'Updated' })
    });
    const result = await lastValueFrom(service.update('123', { title: 'Updated' }));
    expect(result).toEqual({ title: 'Updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { title: 'Updated' }, { new: true });
  });

  it('should delete a video asset', async () => {
    model.findByIdAndDelete.mockReturnValue({
      exec: () => Promise.resolve({ title: 'Deleted' })
    });
    const result = await lastValueFrom(service.delete('123'));
    expect(result).toEqual({ title: 'Deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
