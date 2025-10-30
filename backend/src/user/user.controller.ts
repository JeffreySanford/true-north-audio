import { Controller, Get, Post, Put, Delete, Body, Param } from '@nestjs/common';
import { UserService } from './user.service';
import { User } from '../models/user.model';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}


  @Post()
  create(@Body() data: Partial<User>) {
    return this.userService.create(data);
  }


  @Get()
  findAll() {
    return this.userService.findAll();
  }


  @Get(':id')
  findById(@Param('id') id: string) {
    return this.userService.findById(id);
  }


  @Put(':id')
  update(@Param('id') id: string, @Body() data: Partial<User>) {
    return this.userService.update(id, data);
  }


  @Delete(':id')
  delete(@Param('id') id: string) {
    return this.userService.delete(id);
  }
}
