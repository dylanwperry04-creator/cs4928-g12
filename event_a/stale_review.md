# Event A: stale comment review

For each surviving comment where the nearby code changed, compare the 2021 and 2022 code and decide: is the comment still accurate for the new code?
Fill in `still_accurate` (yes / no) and `note` in `stale_review.csv`. Do this without looking at the model's Event A answers.

## dataset:000004 (Beautification)

2021 (lines 108-108):
```java
105:     /* Only enable AnkiDroid notifications unrelated to due reminders */
106:     public static final int PENDING_NOTIFICATIONS_ONLY = 1000000;
107: 
108:     // Other variables
109:     private final HashMap<String, String> mOriginalSumarries = new HashMap<>();
110:     private static final String [] sCollectionPreferences = {"showEstimates", "showProgress",
111:             "learnCutoff", "timeLimit", "useCurrent", "newSpread", "dayOffset", "schedVer", "newTimezoneHandling"};
```
2022 (lines 120-120):
```java
117:     /* Only enable AnkiDroid notifications unrelated to due reminders */
118:     public static final int PENDING_NOTIFICATIONS_ONLY = 1000000;
119: 
120:     // Other variables
121:     private final HashMap<String, String> mOriginalSumarries = new HashMap<>();
122:     /**
123:      * Represents in Android preferences the collections configuration "estTime": i.e. whether the buttons should indicate the duration of the interval if we click on them.
```

## dataset:000005 (Beautification)

2021 (lines 120-122):
```java
117:     /** The collection path when Preferences was opened  */
118:     private String mOldCollectionPath = null;
119: 
120:     // ----------------------------------------------------------------------------
121:     // Overridden methods
122:     // ----------------------------------------------------------------------------
123:     @Override
124:     protected void onCreate(Bundle savedInstanceState) {
125:         Themes.setThemeLegacy(this);
```
2022 (lines 199-201):
```java
196: 
197:     public static final String EXTRA_SHOW_FRAGMENT = ":android:show_fragment";
198: 
199:     // ----------------------------------------------------------------------------
200:     // Overridden methods
201:     // ----------------------------------------------------------------------------
202:     @Override
203:     protected void onCreate(Bundle savedInstanceState) {
204:         super.onCreate(savedInstanceState);
```

## dataset:000006 (Obvious)

2021 (lines 128-128):
```java
125:         Themes.setThemeLegacy(this);
126:         super.onCreate(savedInstanceState);
127: 
128:         // Add a home button to the actionbar
129:         getSupportActionBar().setHomeButtonEnabled(true);
130:         getSupportActionBar().setDisplayHomeAsUpEnabled(true);
131:         setTitle(getResources().getText(R.string.preferences_title));
```
2022 (lines 210-210):
```java
207: 
208:         enableToolbar();
209: 
210:         // Add a home button to the actionbar
211:         getSupportActionBar().setHomeButtonEnabled(true);
212:         getSupportActionBar().setDisplayHomeAsUpEnabled(true);
213:         setTitle(getResources().getText(R.string.preferences_title));
```

## dataset:000007 (Not a smell)

2021 (lines 133-133):
```java
130:         getSupportActionBar().setDisplayHomeAsUpEnabled(true);
131:         setTitle(getResources().getText(R.string.preferences_title));
132: 
133:         // onRestoreInstanceState takes priority, this is only set on init.
134:         mOldCollectionPath = CollectionHelper.getCollectionPath(this);
135:     }
136: 
```
2022 (lines 217-217):
```java
214: 
215:         Fragment fragment = getInitialFragment(getIntent());
216: 
217:         // onRestoreInstanceState takes priority, this is only set on init.
218:         mOldCollectionPath = CollectionHelper.getCollectionPath(this);
219: 
220:         getSupportFragmentManager()
```

## dataset:000009 (Not a smell)

2021 (lines 183-183):
```java
180: 
181: 
182:     protected void restartWithNewDeckPicker() {
183:         // PERF: DB access on foreground thread
184:         CollectionHelper.getInstance().closeCollection(true, "Preference Modification: collection path changed");
185:         Intent deckPicker = new Intent(this, DeckPicker.class);
186:         deckPicker.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
```
2022 (lines 270-270):
```java
267: 
268:     @SuppressWarnings("deprecation") // startActivity
269:     protected void restartWithNewDeckPicker() {
270:         // PERF: DB access on foreground thread
271:         CollectionHelper.getInstance().closeCollection(true, "Preference Modification: collection path changed");
272:         Intent deckPicker = new Intent(this, DeckPicker.class);
273:         deckPicker.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
```

## dataset:000010 (Beautification)

2021 (lines 210-212):
```java
207:     }
208: 
209: 
210:     // ----------------------------------------------------------------------------
211:     // Class methods
212:     // ----------------------------------------------------------------------------
213: 
214:     public static Intent getPreferenceSubscreenIntent(Context context, String subscreen) {
215:         Intent i = new Intent(context, Preferences.class);
```
2022 (lines 291-293):
```java
288:     }
289: 
290: 
291:     // ----------------------------------------------------------------------------
292:     // Class methods
293:     // ----------------------------------------------------------------------------
294: 
295: 
296:     /**
```

## dataset:000011 (Obvious)

2021 (lines 236-236):
```java
233:                     mCategory.removePreference(mCheckBoxPref_Vibrate);
234:                     mCategory.removePreference(mCheckBoxPref_Blink);
235:                 }
236:                 // Build languages
237:                 initializeLanguageDialog(screen);
238:                 break;
239:             case "com.ichi2.anki.prefs.reviewing":
```
2022 (lines 890-890):
```java
887:                 category.removePreference(checkBoxPref_Vibrate);
888:                 category.removePreference(checkBoxPref_Blink);
889:             }
890:             // Build languages
891:             initializeLanguageDialog(screen);
892:         }
893: 
```

## dataset:000012 (Not a smell)

2021 (lines 242-242):
```java
239:             case "com.ichi2.anki.prefs.reviewing":
240:                 listener.addPreferencesFromResource(R.xml.preferences_reviewing);
241:                 screen = listener.getPreferenceScreen();
242:                 // Show error toast if the user tries to disable answer button without gestures on
243:                 android.preference.ListPreference fullscreenPreference = (android.preference.ListPreference)
244:                         screen.findPreference("fullscreenMode");
245:                 fullscreenPreference.setOnPreferenceChangeListener((preference, newValue) -> {
```
2022 (lines 936-936):
```java
933:         @Override
934:         protected void initSubscreen() {
935:             addPreferencesFromResource(R.xml.preferences_reviewing);
936:             // Show error toast if the user tries to disable answer button without gestures on
937:             Preference buttonsPreference = requirePreference(getString(R.string.answer_buttons_position_preference));
938:             buttonsPreference.setOnPreferenceChangeListener((preference, newValue) -> {
939:                 SharedPreferences prefs = AnkiDroidApp.getSharedPrefs(requireContext());
```

## dataset:000014 (Obvious)

2021 (lines 305-305):
```java
302:                 getSupportActionBar().setTitle(R.string.custom_buttons);
303:                 listener.addPreferencesFromResource(R.xml.preferences_custom_buttons);
304:                 screen = listener.getPreferenceScreen();
305:                 // Reset toolbar button customizations
306:                 android.preference.Preference reset_custom_buttons = screen.findPreference("reset_custom_buttons");
307:                 reset_custom_buttons.setOnPreferenceClickListener(preference -> {
308:                     SharedPreferences.Editor edit = AnkiDroidApp.getSharedPrefs(getBaseContext()).edit();
```
2022 (lines 1411-1411):
```java
1408:         protected void initSubscreen() {
1409:             setTitle(R.string.custom_buttons);
1410:             addPreferencesFromResource(R.xml.preferences_custom_buttons);
1411:             // Reset toolbar button customizations
1412:             Preference reset_custom_buttons = requirePreference("reset_custom_buttons");
1413:             reset_custom_buttons.setOnPreferenceClickListener(preference -> {
1414:                 SharedPreferences.Editor edit = AnkiDroidApp.getSharedPrefs(requireContext()).edit();
```

## dataset:000015 (Commented out code)

2021 (lines 330-330):
```java
327:                     edit.remove("customButtonClearWhiteboard");
328:                     edit.remove("customButtonShowHideWhiteboard");
329:                     edit.apply();
330:                     //finish();
331:                     //TODO: Should reload the preferences screen on completion
332:                     return true;
333:                 });
```
2022 (lines 519-519):
```java
516: 
517:     @SuppressWarnings("deprecation")
518:     private void closePreferences() {
519:         finish();
520:         ActivityTransitionAnimation.slide(this, FADE);
521:         if (getCol() != null && getCol().getDb()!= null) {
522:             getCol().save();
```

## dataset:000017 (Not a smell)

2021 (lines 338-338):
```java
335:             case "com.ichi2.anki.prefs.advanced":
336:                 listener.addPreferencesFromResource(R.xml.preferences_advanced);
337:                 screen = listener.getPreferenceScreen();
338:                 // Check that input is valid before committing change in the collection path
339:                 android.preference.EditTextPreference collectionPathPreference = (android.preference.EditTextPreference) screen.findPreference("deckPath");
340:                 collectionPathPreference.setOnPreferenceChangeListener((preference, newValue) -> {
341:                     final String newPath = (String) newValue;
```
2022 (lines 1156-1156):
```java
1153:         protected void initSubscreen() {
1154:             addPreferencesFromResource(R.xml.preferences_advanced);
1155:             PreferenceScreen screen = getPreferenceScreen();
1156:             // Check that input is valid before committing change in the collection path
1157:             EditTextPreference collectionPathPreference = requirePreference(CollectionHelper.PREF_DECK_PATH);
1158:             collectionPathPreference.setOnPreferenceChangeListener((preference, newValue) -> {
1159:                 final String newPath = (String) newValue;
```

## dataset:000020 (Obvious)

2021 (lines 376-376):
```java
373:                 setupContextMenuPreference(screen, CardBrowserContextMenu.CARD_BROWSER_CONTEXT_MENU_PREF_KEY, R.string.card_browser_context_menu);
374:                 setupContextMenuPreference(screen, AnkiCardContextMenu.ANKI_CARD_CONTEXT_MENU_PREF_KEY, R.string.context_menu_anki_card_label);
375: 
376:                 // Make it possible to test crash reporting, but only for DEBUG builds
377:                 if (BuildConfig.DEBUG && !AdaptionUtil.isUserATestClient()) {
378:                     Timber.i("Debug mode, allowing for test crashes");
379:                     android.preference.Preference triggerTestCrashPreference = new android.preference.Preference(this);
```
2022 (lines 1219-1219):
```java
1216:             }
1217: 
1218: 
1219:             // Make it possible to test crash reporting, but only for DEBUG builds
1220:             if (BuildConfig.DEBUG && !AdaptionUtil.isUserATestClient()) {
1221:                 Timber.i("Debug mode, allowing for test crashes");
1222:                 Preference triggerTestCrashPreference = new Preference(requireContext());
```

## dataset:000021 (Obvious)

2021 (lines 389-389):
```java
386:                     });
387:                     screen.addPreference(triggerTestCrashPreference);
388:                 }
389:                 // Make it possible to test analytics, but only for DEBUG builds
390:                 if (BuildConfig.DEBUG) {
391:                     Timber.i("Debug mode, allowing for dynamic analytics config");
392:                     android.preference.Preference analyticsDebugMode = new android.preference.Preference(this);
```
2022 (lines 1232-1232):
```java
1229:                 });
1230:                 screen.addPreference(triggerTestCrashPreference);
1231:             }
1232:             // Make it possible to test analytics, but only for DEBUG builds
1233:             if (BuildConfig.DEBUG) {
1234:                 Timber.i("Debug mode, allowing for dynamic analytics config");
1235:                 Preference analyticsDebugMode = new Preference(requireContext());
```

## dataset:000022 (Obvious)

2021 (lines 419-419):
```java
416:                     });
417:                     screen.addPreference(lockDbPreference);
418:                 }
419:                 // Adding change logs in both debug and release builds
420:                 Timber.i("Adding open changelog");
421:                 android.preference.Preference changelogPreference = new android.preference.Preference(this);
422:                 changelogPreference.setTitle(R.string.open_changelog);
```
2022 (lines 1311-1311):
```java
1308:                 });
1309:                 screen.addPreference(onboardingPreference);
1310:             }
1311:             // Adding change logs in both debug and release builds
1312:             Timber.i("Adding open changelog");
1313:             Preference changelogPreference = new Preference(requireContext());
1314:             changelogPreference.setTitle(R.string.open_changelog);
```

## dataset:000023 (Obvious)

2021 (lines 427-427):
```java
424:                 infoIntent.putExtra(Info.TYPE_EXTRA, Info.TYPE_NEW_VERSION);
425:                 changelogPreference.setIntent(infoIntent);
426:                 screen.addPreference(changelogPreference);
427:                 // Force full sync option
428:                 ConfirmationPreference fullSyncPreference = (ConfirmationPreference)screen.findPreference("force_full_sync");
429:                 fullSyncPreference.setDialogMessage(R.string.force_full_sync_summary);
430:                 fullSyncPreference.setDialogTitle(R.string.force_full_sync_title);
```
2022 (lines 1319-1319):
```java
1316:             infoIntent.putExtra(Info.TYPE_EXTRA, Info.TYPE_NEW_VERSION);
1317:             changelogPreference.setIntent(infoIntent);
1318:             screen.addPreference(changelogPreference);
1319:             // Force full sync option
1320:             ConfirmationPreferenceCompat fullSyncPreference = requirePreference("force_full_sync");
1321:             fullSyncPreference.setDialogMessage(R.string.force_full_sync_summary);
1322:             fullSyncPreference.setDialogTitle(R.string.force_full_sync_title);
```

## dataset:000024 (Not a smell)

2021 (lines 440-440):
```java
437:                     getCol().setMod();
438:                     UIUtils.showThemedToast(getApplicationContext(), android.R.string.ok, true);
439:                 });
440:                 // Workaround preferences
441:                 removeUnnecessaryAdvancedPrefs(screen);
442:                 addThirdPartyAppsListener(screen);
443:                 break;
```
2022 (lines 1332-1332):
```java
1329:                 getCol().setMod();
1330:                 UIUtils.showThemedToast(requireContext(), android.R.string.ok, true);
1331:             });
1332:             // Workaround preferences
1333:             removeUnnecessaryAdvancedPrefs();
1334:             addThirdPartyAppsListener();
1335:         }
```

## dataset:000025 (Task)

2021 (lines 486-487):
```java
483: 
484: 
485:     private void setupContextMenuPreference(android.preference.PreferenceScreen screen, String key, @StringRes int contextMenuName) {
486:         // FIXME: The menu is named in the system language (as it's defined in the manifest which may be
487:         //  different than the app language
488:         android.preference.CheckBoxPreference cardBrowserContextMenuPreference = (android.preference.CheckBoxPreference) screen.findPreference(key);
489:         String menuName = getString(contextMenuName);
490:         // Note: The below format strings are generic, not card browser specific despite the name
```
2022 (lines 1338-1339):
```java
1335:         }
1336: 
1337:         private void setupContextMenuPreference(String key, @StringRes int contextMenuName) {
1338:             // FIXME: The menu is named in the system language (as it's defined in the manifest which may be
1339:             //  different than the app language
1340:             CheckBoxPreference cardBrowserContextMenuPreference = requirePreference(key);
1341:             String menuName = getString(contextMenuName);
1342:             // Note: The below format strings are generic, not card browser specific despite the name
```

## dataset:000026 (Not a smell)

2021 (lines 490-490):
```java
487:         //  different than the app language
488:         android.preference.CheckBoxPreference cardBrowserContextMenuPreference = (android.preference.CheckBoxPreference) screen.findPreference(key);
489:         String menuName = getString(contextMenuName);
490:         // Note: The below format strings are generic, not card browser specific despite the name
491:         cardBrowserContextMenuPreference.setTitle(getString(R.string.card_browser_enable_external_context_menu, menuName));
492:         cardBrowserContextMenuPreference.setSummary(getString(R.string.card_browser_enable_external_context_menu_summary, menuName));
493:     }
```
2022 (lines 1342-1342):
```java
1339:             //  different than the app language
1340:             CheckBoxPreference cardBrowserContextMenuPreference = requirePreference(key);
1341:             String menuName = getString(contextMenuName);
1342:             // Note: The below format strings are generic, not card browser specific despite the name
1343:             cardBrowserContextMenuPreference.setTitle(getString(R.string.card_browser_enable_external_context_menu, menuName));
1344:             cardBrowserContextMenuPreference.setSummary(getString(R.string.card_browser_enable_external_context_menu_summary, menuName));
1345:         }
```

## dataset:000027 (Task)

2021 (lines 499-499):
```java
496:     @Override
497:     protected void onActivityResult(int requestCode, int resultCode, Intent data) {
498:         super.onActivityResult(requestCode, resultCode, data);
499:         // DEFECT #5973: Does not handle Google Drive downloads
500:         try {
501:             if (requestCode == RESULT_LOAD_IMG && resultCode == RESULT_OK && null != data) {
502:                 Uri selectedImage = data.getData();
```
2022 (lines 1055-1055):
```java
1052:         @Override
1053:         public void onActivityResult(int requestCode, int resultCode, Intent data) {
1054:             super.onActivityResult(requestCode, resultCode, data);
1055:             // DEFECT #5973: Does not handle Google Drive downloads
1056:             try {
1057:                 if (requestCode == RESULT_LOAD_IMG && resultCode == RESULT_OK && null != data) {
1058:                     Uri selectedImage = data.getData();
```

## dataset:000028 (Not a smell)

2021 (lines 510-510):
```java
507:                     String imgPathString = cursor.getString(columnIndex);
508:                     File sourceFile = new File(imgPathString);
509: 
510:                     // file size in MB
511:                     long fileLength = sourceFile.length() / (1024 * 1024);
512: 
513:                     String currentAnkiDroidDirectory = CollectionHelper.getCurrentAnkiDroidDirectory(this);
```
2022 (lines 1062-1062):
```java
1059:                     String[] filePathColumn = { MediaStore.MediaColumns.SIZE };
1060:                     try (Cursor cursor = requireContext().getContentResolver().query(selectedImage, filePathColumn, null, null, null)) {
1061:                         cursor.moveToFirst();
1062:                         // file size in MB
1063:                         long fileLength = cursor.getLong(0) / (1024 * 1024);
1064: 
1065:                         String currentAnkiDroidDirectory = CollectionHelper.getCurrentAnkiDroidDirectory(requireContext());
```

## dataset:000029 (Not a smell)

2021 (lines 516-516):
```java
513:                     String currentAnkiDroidDirectory = CollectionHelper.getCurrentAnkiDroidDirectory(this);
514:                     String imageName = "DeckPickerBackground.png";
515:                     File destFile = new File(currentAnkiDroidDirectory, imageName);
516:                     // Image size less than 10 MB copied to AnkiDroid folder
517:                     if (fileLength < 10) {
518:                         try (FileChannel sourceChannel = new FileInputStream(sourceFile).getChannel();
519:                              FileChannel destChannel = new FileOutputStream(destFile).getChannel()) {
```
2022 (lines 1068-1068):
```java
1065:                         String currentAnkiDroidDirectory = CollectionHelper.getCurrentAnkiDroidDirectory(requireContext());
1066:                         String imageName = "DeckPickerBackground.png";
1067:                         File destFile = new File(currentAnkiDroidDirectory, imageName);
1068:                         // Image size less than 10 MB copied to AnkiDroid folder
1069:                         if (fileLength < 10) {
1070:                             try (FileChannel sourceChannel = ((FileInputStream) requireContext().getContentResolver().openInputStream(selectedImage)).getChannel();
1071:                                  FileChannel destChannel = new FileOutputStream(destFile).getChannel()) {
```

## dataset:000030 (Task)

2021 (lines 539-540):
```java
536:     }
537: 
538:     private void addThirdPartyAppsListener(android.preference.PreferenceScreen screen) {
539:         //#5864 - some people don't have a browser so we can't use <intent>
540:         //and need to handle the keypress ourself.
541:         android.preference.Preference showThirdParty = screen.findPreference("thirdpartyapps_link");
542:         final String githubThirdPartyAppsUrl = "https://github.com/ankidroid/Anki-Android/wiki/Third-Party-Apps";
543:         showThirdParty.setOnPreferenceClickListener((preference) -> {
```
2022 (lines 1367-1368):
```java
1364: 
1365: 
1366:         private void addThirdPartyAppsListener() {
1367:             // #5864 - some people don't have a browser so we can't use <intent>
1368:             // and need to handle the keypress ourself.
1369:             Preference showThirdParty = requirePreference("thirdpartyapps_link");
1370:             final String githubThirdPartyAppsUrl = "https://github.com/ankidroid/Anki-Android/wiki/Third-Party-Apps";
1371:             showThirdParty.setOnPreferenceClickListener((preference) -> {
```

## dataset:000031 (Not a smell)

2021 (lines 549-549):
```java
546:                 super.startActivity(openThirdPartyAppsIntent);
547:             } catch (ActivityNotFoundException e) {
548:                 Timber.w(e);
549:                 //We use a different message here. We have limited space in the snackbar
550:                 String error = getString(R.string.activity_start_failed_load_url, githubThirdPartyAppsUrl);
551:                 UIUtils.showSimpleSnackbar(this, error, false);
552:             }
```
2022 (lines 1377-1377):
```java
1374:                     super.startActivity(openThirdPartyAppsIntent);
1375:                 } catch (ActivityNotFoundException e) {
1376:                     Timber.w(e);
1377:                     //We use a different message here. We have limited space in the snackbar
1378:                     String error = getString(R.string.activity_start_failed_load_url, githubThirdPartyAppsUrl);
1379:                     UIUtils.showSimpleSnackbar(getActivity(), error, false);
1380:                 }
```

## dataset:000032 (Obvious)

2021 (lines 586-586):
```java
583: 
584: 
585:     private void initPreference(android.preference.Preference pref) {
586:         // Load stored values from Preferences which are stored in the Collection
587:         if (Arrays.asList(sCollectionPreferences).contains(pref.getKey())) {
588:             Collection col = getCol();
589:             if (col != null) {
```
2022 (lines 324-324):
```java
321: 
322: 
323:     private void initPreference(Preference pref) {
324:         // Load stored values from Preferences which are stored in the Collection
325:         if (Arrays.asList(sCollectionPreferences).contains(pref.getKey())) {
326:             Collection col = getCol();
327:             if (col != null) {
```

## dataset:000033 (Obvious)

2021 (lines 629-629):
```java
626:                     throw new RuntimeException(e);
627:                 }
628:             } else {
629:                 // Disable Col preferences if Collection closed
630:                 pref.setEnabled(false);
631:             }
632:         } else if ("minimumCardsDueForNotification".equals(pref.getKey())) {
```
2022 (lines 370-370):
```java
367:                     throw new RuntimeException(e);
368:                 }
369:             } else {
370:                 // Disable Col preferences if Collection closed
371:                 pref.setEnabled(false);
372:             }
373:         } else if (MINIMUM_CARDS_DUE_FOR_NOTIFICATION.equals(pref.getKey())) {
```

## dataset:000034 (Obvious)

2021 (lines 635-635):
```java
632:         } else if ("minimumCardsDueForNotification".equals(pref.getKey())) {
633:             updateNotificationPreference((android.preference.ListPreference) pref);
634:         }
635:         // Set the value from the summary cache
636:         CharSequence s = pref.getSummary();
637:         mOriginalSumarries.put(pref.getKey(), (s != null) ? s.toString() : "");
638:         // Update summary
```
2022 (lines 376-376):
```java
373:         } else if (MINIMUM_CARDS_DUE_FOR_NOTIFICATION.equals(pref.getKey())) {
374:             updateNotificationPreference((ListPreference) pref);
375:         }
376:         // Set the value from the summary cache
377:         CharSequence s = pref.getSummary();
378:         mOriginalSumarries.put(pref.getKey(), (s != null) ? s.toString() : "");
379:         // Update summary
```

## dataset:000038 (Not a smell)

2021 (lines 703-703):
```java
700:                 case CustomSyncServer.PREFERENCE_CUSTOM_MEDIA_SYNC_URL:
701:                 case CustomSyncServer.PREFERENCE_CUSTOM_SYNC_BASE:
702:                 case CustomSyncServer.PREFERENCE_ENABLE_CUSTOM_SYNC_SERVER:
703:                     //This may be a tad hasty - performed before "back" is pressed.
704:                     CustomSyncServer.handleSyncServerPreferenceChange(getBaseContext());
705:                     break;
706:                 case "timeoutAnswer": {
```
2022 (lines 661-661):
```java
658:                     case CustomSyncServer.PREFERENCE_CUSTOM_MEDIA_SYNC_URL:
659:                     case CustomSyncServer.PREFERENCE_CUSTOM_SYNC_BASE:
660:                     case CustomSyncServer.PREFERENCE_ENABLE_CUSTOM_SYNC_SERVER:
661:                         //This may be a tad hasty - performed before "back" is pressed.
662:                         CustomSyncServer.handleSyncServerPreferenceChange(preferencesActivity.getBaseContext());
663:                         break;
664:                     case "timeoutAnswer": {
```

## dataset:000043 (Not a smell)

2021 (lines 830-830):
```java
827:                                 getCol().changeSchedulerVer(1);
828:                                 ((android.preference.CheckBoxPreference) pref).setChecked(false);
829:                             } catch (ConfirmModSchemaException e2) {
830:                                 // This should never be reached as we explicitly called modSchemaNoCheck()
831:                                 throw new RuntimeException(e2);
832:                             }
833:                         });
```
2022 (lines 1195-1195):
```java
1192:                             getCol().changeSchedulerVer(2);
1193:                             screen.removePreference(schedVerPreference);
1194:                         } catch (ConfirmModSchemaException e2) {
1195:                             // This should never be reached as we explicitly called modSchemaNoCheck()
1196:                             throw new RuntimeException(e2);
1197:                         }
1198:                     });
```

## dataset:000044 (Obvious)

2021 (lines 840-840):
```java
837:                         builder.show();
838:                         break;
839:                     }
840:                     // Going to V2
841:                     builder.title(R.string.sched_ver_toggle_title);
842:                     builder.content(R.string.sched_ver_1to2);
843:                     builder.onPositive((dialog, which) -> {
```
2022 (lines 1186-1186):
```java
1183:                 schedVerPreference.setOnPreferenceChangeListener((preference, o) -> {
1184: 
1185:                     MaterialDialog.Builder builder = new MaterialDialog.Builder(requireContext());
1186:                     // Going to V2
1187:                     builder.title(R.string.sched_ver_toggle_title);
1188:                     builder.content(R.string.sched_ver_1to2);
1189:                     builder.onPositive((dialog, which) -> {
```

## dataset:000046 (Obvious)

2021 (lines 869-869):
```java
866:                     updateGestureCornerTouch(screen);
867:                 }
868:             }
869:             // Update the summary text to reflect new value
870:             updateSummary(pref);
871:         } catch (BadTokenException e) {
872:             Timber.e(e, "Preferences: BadTokenException on showDialog");
```
2022 (lines 784-784):
```java
781:                         GesturesSettingsFragment.updateGestureCornerTouch(preferencesActivity, screen);
782:                     }
783:                 }
784:                 // Update the summary text to reflect new value
785:                 preferencesActivity.updateSummary(pref);
786:             } catch (BadTokenException e) {
787:                 Timber.e(e, "Preferences: BadTokenException on showDialog");
```

## dataset:000048 (Obvious)

2021 (lines 933-933):
```java
930:                 }
931:                 break;
932:         }
933:         // Get value text
934:         String value;
935:         try {
936:             if (pref instanceof  NumberRangePreference) {
```
2022 (lines 462-462):
```java
459:                 }
460:                 break;
461:         }
462:         // Get value text
463:         String value;
464:         try {
465:             if (pref instanceof ControlPreference) {
```

