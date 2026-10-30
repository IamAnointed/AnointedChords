# Anoint Chords — Android APK project

## Build via GitHub
Upload the **contents** of this folder to a GitHub repository (preserve `.github/workflows/build-apk.yml`). Open Actions → Build Anoint Chords APK → Run workflow. Download `Anoint-Chords-debug-apk` from the completed run. Debug APK is for testing, not Play Store distribution.

## CRITICAL Firebase setup before using
1. Existing Firebase project in index.html is `chord-charts-bd4c3`. Confirm you own it.
2. In Firebase Console → Authentication, enable Email/Password, create ONE admin account, copy its UID. **Never share the password.**
3. Replace `REPLACE_WITH_ADMIN_FIREBASE_UID` in `app/src/main/assets/index.html` and `firestore.rules` with that UID.
4. Deploy `firestore.rules` using Firebase Console → Firestore Database → Rules → Publish. **UI-only restrictions are NOT security.**
5. Test with viewer (no login) and admin account. Firebase rules must permit public reads. Beware that this makes all song data publicly readable to anyone with Firebase project details.
6. Existing Firebase songs are NOT modified by building this project. No Drive files are imported automatically.

## Source-only Excel import
Use `import-tools/convert_source.py` on a ZIP containing the Drive `.xlsx` files, review `songs.json` and `review.csv`, then paste the reviewed JSON into Admin → Import Songs. Import is additive; avoid duplicate uploads.

## Limitations
The original app stores chord-count grids, not lyric text. Excel extraction is best-effort and needs human review. Online Firebase sync requires internet. The app uses CDN-hosted Firebase scripts and therefore first-time offline use is not supported. Android WebView behavior should be tested on device. Existing Firestore rules must be replaced to enable guest reads and admin-only writes.
