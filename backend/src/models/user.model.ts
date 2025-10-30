import { Schema, Document, model } from 'mongoose';

export type UserRole = 'admin' | 'user';

export interface User extends Document {
  username: string;
  roles: UserRole[];
}

const UserSchema = new Schema<User>({
  username: { type: String, required: true, unique: true },
  roles: { type: [String], enum: ['admin', 'user'], default: ['user'] },
});

export const UserModel = model<User>('User', UserSchema);
