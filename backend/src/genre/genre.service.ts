
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { Genre } from '../models/genre.model';
import { ReplaySubject } from 'rxjs';

@Injectable()
export class GenreService {
  // Remove persistent Subjects; use per-call ReplaySubject(1)

  constructor(@InjectModel('Genre') private readonly genreModel: Model<Genre>) {}

  create(data: Partial<Genre>) {
    const subject = new ReplaySubject<Genre>(1);
    this.genreModel.create(data)
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  findAll() {
    const subject = new ReplaySubject<Genre[]>(1);
    this.genreModel.find().exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  findById(id: string) {
    const subject = new ReplaySubject<Genre | null>(1);
    this.genreModel.findById(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  update(id: string, data: Partial<Genre>) {
    const subject = new ReplaySubject<Genre | null>(1);
    this.genreModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }

  delete(id: string) {
    const subject = new ReplaySubject<Genre | null>(1);
    this.genreModel.findByIdAndDelete(id).exec()
      .then(result => {
        subject.next(result);
        subject.complete();
      })
      .catch(err => subject.error(err));
    return subject.asObservable();
  }
}
