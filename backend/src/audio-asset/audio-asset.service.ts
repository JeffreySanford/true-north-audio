
import { Injectable } from '@nestjs/common';
import { InjectModel } from '@nestjs/mongoose';
import { Model } from 'mongoose';
import { AudioAsset } from '../models/audio-asset.model';
import { Subject } from 'rxjs';


/**
 * Service for managing audio assets in the database.
 * Provides CRUD operations using RxJS hot observables.
 *
 * Usage:
 *   Inject AudioAssetService and call methods for asset management.
 */
@Injectable()
export class AudioAssetService {
  private createSubject = new Subject<AudioAsset>();
  private findAllSubject = new Subject<AudioAsset[]>();
  private findByIdSubject = new Subject<AudioAsset | null>();
  private updateSubject = new Subject<AudioAsset | null>();
  private deleteSubject = new Subject<AudioAsset | null>();

  /**
   * Injects the AudioAsset Mongoose model.
   * @param audioAssetModel Mongoose model for AudioAsset
   */
  constructor(@InjectModel('AudioAsset') private readonly audioAssetModel: Model<AudioAsset>) {}

  /**
   * Create a new audio asset.
   * @param data Partial audio asset data
   * @returns Observable emitting the created asset
   */
  create(data: Partial<AudioAsset>) {
    this.audioAssetModel.create(data)
      .then(result => this.createSubject.next(result))
      .catch(err => this.createSubject.error(err));
    return this.createSubject.asObservable();
  }

  /**
   * Find all audio assets.
   * @returns Observable emitting array of assets
   */
  findAll() {
    this.audioAssetModel.find().populate('genre').populate('vocalFeatures').exec()
      .then(result => this.findAllSubject.next(result))
      .catch(err => this.findAllSubject.error(err));
    return this.findAllSubject.asObservable();
  }

  /**
   * Find an audio asset by ID.
   * @param id Asset ID
   * @returns Observable emitting the found asset or null
   */
  findById(id: string) {
    this.audioAssetModel.findById(id).populate('genre').populate('vocalFeatures').exec()
      .then(result => this.findByIdSubject.next(result))
      .catch(err => this.findByIdSubject.error(err));
    return this.findByIdSubject.asObservable();
  }

  /**
   * Update an audio asset by ID.
   * @param id Asset ID
   * @param data Partial asset data
   * @returns Observable emitting the updated asset or null
   */
  update(id: string, data: Partial<AudioAsset>) {
    this.audioAssetModel.findByIdAndUpdate(id, data, { new: true }).exec()
      .then(result => this.updateSubject.next(result))
      .catch(err => this.updateSubject.error(err));
    return this.updateSubject.asObservable();
  }

  /**
   * Delete an audio asset by ID.
   * @param id Asset ID
   * @returns Observable emitting the deleted asset or null
   */
  delete(id: string) {
    this.audioAssetModel.findByIdAndDelete(id).exec()
      .then(result => this.deleteSubject.next(result))
      .catch(err => this.deleteSubject.error(err));
    return this.deleteSubject.asObservable();
  }
}
