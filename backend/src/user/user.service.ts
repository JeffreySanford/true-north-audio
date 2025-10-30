
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { User } from '../models/user.model';
import { ReplaySubject, Subject } from 'rxjs';

@Injectable()
export class UserService {

  constructor(@InjectModel('User') private readonly userModel: Model<User>) {}

  create(data: Partial<User>) {
    this.userModel.create(data)
    const subject = new ReplaySubject(1);
    this.userModel.create(data)
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  findAll() {
    this.userModel.find().exec()
    const subject = new ReplaySubject(1);
    this.userModel.find().exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  findById(id: string) {
    this.userModel.findById(id).exec()
    const subject = new ReplaySubject(1);
    this.userModel.findById(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  update(id: string, data: Partial<User>) {
    this.userModel.findByIdAndUpdate(id, data, { new: true }).exec()
    const subject = new ReplaySubject(1);
    this.userModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  delete(id: string) {
    this.userModel.findByIdAndDelete(id).exec()
    const subject = new ReplaySubject(1);
    this.userModel.findByIdAndDelete(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }
}
