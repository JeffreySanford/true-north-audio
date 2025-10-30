import { Test, TestingModule } from '@nestjs/testing';
import { getModelToken } from '@nestjs/mongoose';
import { UserService } from './user.service';

const mockUserModel = {
  create: jest.fn(),
  find: jest.fn().mockReturnThis(),
  exec: jest.fn(),
  findById: jest.fn().mockReturnThis(),
  findByIdAndUpdate: jest.fn().mockReturnThis(),
  findByIdAndDelete: jest.fn().mockReturnThis(),
};

describe('UserService', () => {
  let service: UserService;
  let model: typeof mockUserModel;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        { provide: getModelToken('User'), useValue: mockUserModel },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    model = module.get(getModelToken('User'));
  });

  it('should create a user', async () => {
    model.create.mockResolvedValue({ username: 'user1' });
    const result = await service.create({ username: 'user1' });
    expect(result).toEqual({ username: 'user1' });
    expect(model.create).toHaveBeenCalledWith({ username: 'user1' });
  });

  it('should find all users', async () => {
    model.find.mockReturnValue({ exec: () => Promise.resolve([{ username: 'user2' }]) });
    const result = await service.findAll();
    expect(result).toEqual([{ username: 'user2' }]);
  });

  it('should find a user by id', async () => {
    model.findById.mockReturnValue({ exec: () => Promise.resolve({ username: 'user3' }) });
    const result = await service.findById('123');
    expect(result).toEqual({ username: 'user3' });
    expect(model.findById).toHaveBeenCalledWith('123');
  });

  it('should update a user', async () => {
    model.findByIdAndUpdate.mockReturnValue({ exec: () => Promise.resolve({ username: 'updated' }) });
    const result = await service.update('123', { username: 'updated' });
    expect(result).toEqual({ username: 'updated' });
    expect(model.findByIdAndUpdate).toHaveBeenCalledWith('123', { username: 'updated' }, { new: true });
  });

  it('should delete a user', async () => {
    model.findByIdAndDelete.mockReturnValue({ exec: () => Promise.resolve({ username: 'deleted' }) });
    const result = await service.delete('123');
    expect(result).toEqual({ username: 'deleted' });
    expect(model.findByIdAndDelete).toHaveBeenCalledWith('123');
  });
});
