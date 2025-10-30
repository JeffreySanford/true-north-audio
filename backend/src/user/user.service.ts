
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { User } from '../models/user.model';
import { Subject } from 'rxjs';

@Injectable()
export class UserService {
  private createSubject = new Subject<User>();
  private findAllSubject = new Subject<User[]>();
  private findByIdSubject = new Subject<User | null>();
  private updateSubject = new Subject<User | null>();
  private deleteSubject = new Subject<User | null>();

  constructor(@InjectModel('User') private readonly userModel: Model<User>) {}

  create(data: Partial<User>) {
    this.userModel.create(data)
      .then(result => this.createSubject.next(result))
      .catch(err => this.createSubject.error(err));
    return this.createSubject.asObservable();
  }

  findAll() {
    this.userModel.find().exec()
      .then(result => this.findAllSubject.next(result))
      .catch(err => this.findAllSubject.error(err));
    return this.findAllSubject.asObservable();
  }

  findById(id: string) {
    this.userModel.findById(id).exec()
      .then(result => this.findByIdSubject.next(result))
      .catch(err => this.findByIdSubject.error(err));
    return this.findByIdSubject.asObservable();
  }

  update(id: string, data: Partial<User>) {
    this.userModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => this.updateSubject.next(result))
      .catch(err => this.updateSubject.error(err));
    return this.updateSubject.asObservable();
  }

  delete(id: string) {
    this.userModel.findByIdAndDelete(id).exec()
      .then(result => this.deleteSubject.next(result))
      .catch(err => this.deleteSubject.error(err));
    return this.deleteSubject.asObservable();
  }
}
