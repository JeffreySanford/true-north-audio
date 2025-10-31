import { Test, TestingModule } from '@nestjs/testing';
import { lastValueFrom } from 'rxjs';
import { getModelToken } from '@nestjs/mongoose';
import { GenreService } from './genre.service';

const mockGenreModel = {
  create: jest.fn(),
  find: jest.fn(),
  findById: jest.fn(),
  findByIdAndUpdate: jest.fn(),
  findByIdAndDelete: jest.fn(),
};

describe('GenreService', () => {
  let service: GenreService;
  let model: typeof mockGenreModel;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        GenreService,
        { provide: getModelToken('Genre'), useValue: mockGenreModel },
      ],
    }).compile();

    service = module.get<GenreService>(GenreService);
    model = module.get(getModelToken('Genre'));
  });

  it('should create a genre', async () => {
    model.create.mockReturnValue({
  then: (cb: (genre: { name: string }) => void) => { setTimeout(() => cb({ name: 'Rock' }), 0); return { catch: () => {} }; }
    });
    const result = await lastValueFrom(service.create({ name: 'Rock' }));
    expect(result).toEqual({ name: 'Rock' });
    expect(model.create).toHaveBeenCalledWith({ name: 'Rock' });
  });

  it('should find all genres', async () => {
    model.find.mockReturnValue({
      exec: () => Promise.resolve([{ name: 'Jazz' }])
    });
    const result = await lastValueFrom(service.findAll());
    expect(result).toEqual([{ name: 'Jazz' }]);
  });

  it('should find a genre by id', async () => {
    model.findById.mockReturnValue({
      exec: () => Promise.resolve({ name: 'Pop' })
    });
    const result = await lastValueFrom(service.findById('123'));
    expect(result).toEqual({ name: 'Pop' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  it('should update a genre', async () => {
    model.findByIdAndUpdate.mockReturnValue({
      exec: () => ({
  then: (cb: (genre: { name: string }) => void) => { setTimeout(() => cb({ name: 'Updated' }), 0); return { catch: () => {} }; }
      })
    });
    const result = await lastValueFrom(service.update('123', { name: 'Updated' }));
    expect(result).toEqual({ name: 'Updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { name: 'Updated' }, { new: true });
  });

  it('should delete a genre', async () => {
    model.findByIdAndDelete.mockReturnValue({
      exec: () => ({
  then: (cb: (genre: { name: string }) => void) => { setTimeout(() => cb({ name: 'Deleted' }), 0); return { catch: () => {} }; }
      })
    });
    const result = await lastValueFrom(service.delete('123'));
    expect(result).toEqual({ name: 'Deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
