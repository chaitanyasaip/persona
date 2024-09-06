import { initializeApp } from 'firebase/app';
import { getDatabase } from 'firebase/database';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
  // Your web app's Firebase configuration
  // Copy this from your Firebase project settings
  apiKey: "AIzaSyAgYRMFpdNtVuzjmEBkSzWQutfjt7EVefw",
  authDomain: "persona-22e8d.firebaseapp.com",
  projectId: "persona-22e8d",
  storageBucket: "persona-22e8d.appspot.com",
  messagingSenderId: "975554770226",
  appId: "1:975554770226:web:266603d6d97905ffa3532b",
  measurementId: "G-2NRLZ98ZZF"
};
// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getDatabase(app);