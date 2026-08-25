# iPhone Image and Video Deduplication & Consolidation Tool

A safe, non-destructive Python utility for scanning an iPhone image and video import directory, identifying exact duplicates and potential near-duplicates, and creating a clean consolidated copy of the media collection.

The project is designed for situations where photos have been imported from an iPhone multiple times into different folders, resulting in duplicate files, different filenames, different filesystem dates, different metadata, resized copies, recompressed copies, and other variations.

> **IMPORTANT: This project is COPY-ONLY.**
>
> The original source directory and all files inside it are treated as **read-only**. The program never deletes, moves, renames, or modifies source files. It only reads from the source and copies selected files into a newly created output directory.

---

## 1. Objective

The objective is to create a clean, consolidated image collection from multiple iPhone import folders while preserving the original collection completely unchanged.

For example, the source may look like:

```text
D:\Data\Pictures\iphone
│
├── Import_01
│   ├── IMG_0001.JPG
│   ├── IMG_0002.HEIC
│   └── IMG_0003.JPG
│
├── Import_02
│   ├── IMG_0001.JPG
│   ├── IMG_0002.HEIC
│   └── IMG_0004.JPG
│
└── Import_03
    ├── IMG_0001.JPG
    ├── IMG_0005.JPG
    └── IMG_0006.HEIC
```

After processing, a new directory is created:

```text
D:\Data\Pictures
│
├── iphone
│   ├── Import_01
│   ├── Import_02
│   └── Import_03
│
└── iphone_cleaned_YYYY-MM-DD_HHMMSS
    ├── Images
    ├── Review
    └── Reports
```

The original `iphone` directory remains untouched.

---

# 2. Core Safety Principle

The program follows a strict:

## READ → ANALYZE → SELECT → COPY

workflow.

It does **not** perform:

```text
DELETE
MOVE
RENAME SOURCE
MODIFY SOURCE
```

### The program WILL

- Recursively scan the source directory.
- Identify supported image files.
- Read file metadata.
- Read EXIF metadata where available.
- Calculate SHA-256 hashes.
- Identify exact duplicate files.
- Identify same-name/different-content files.
- Identify potential near-duplicates.
- Generate reports.
- Create a new output directory.
- Copy selected files to the output directory.
- Verify copied files where enabled.

### The program WILL NOT

- Delete source files.
- Move source files.
- Rename source files.
- Modify source files.
- Modify EXIF metadata.
- Compress source files.
- Resize source files.
- Convert source files.
- Change source folder structure.
- Overwrite source files.

---

# 3. Source Directory

The default source directory is:

```text
D:\Data\Pictures\iphone
```

The source directory can contain any number of subdirectories.

The scanner recursively processes the entire directory tree.

Example:

```text
D:\Data\Pictures\iphone
├── Folder_A
├── Folder_B
├── Folder_C
└── Folder_D
```

All supported images under these directories are considered during analysis.

---

# 4. Output Directory

The program creates a **new directory outside the source directory**.

Recommended naming:

```text
iphone_cleaned_YYYY-MM-DD_HHMMSS
```

Example:

```text
D:\Data\Pictures\iphone_cleaned_2026-08-23_123000
```

The output directory is created as a separate collection.

The original directory remains unchanged.

---

# 5. Output Directory Structure

Recommended output:

```text
iphone_cleaned_YYYY-MM-DD_HHMMSS
│
├── Images
│   └── Final consolidated images
│
├── Review
│   ├── Near_Duplicates
│   └── Possible_Edits
│
└── Reports
    ├── scan_report.csv
    ├── duplicate_report.csv
    ├── review_report.csv
    └── summary.txt
```

## Images

Contains the final selected image collection.

Only one representative is copied for an exact duplicate group.

Different images are retained.

## Review

Contains ambiguous cases that should not be automatically discarded.

Examples:

- Resized images
- Recompressed images
- Visually similar images
- Possible edited versions

## Reports

Contains detailed information about the scan and decisions.

---

# 6. Supported Image Formats

The application should support common iPhone and general image formats, including:

```text
.jpg
.jpeg
.heic
.heif
.png
.webp
.tif
.tiff
.bmp
.gif
.mov
.mp4
.m4v
.avi
.mkv
.3gp
```

Video files are scanned, hashed, deduplicated by exact content, copied, and verified using the same conservative copy-only workflow as images. The supported extensions can be configured.

Non-image files are ignored unless explicitly configured otherwise.

---

# 7. Duplicate Detection Philosophy

The tool uses multiple levels of analysis.

The most important distinction is:

> **Exact duplicate ≠ visually similar image**

A cryptographic hash such as SHA-256 is used to identify files with identical binary content.

Perceptual/visual hashing can optionally be used to identify images that look similar even though their binary content is different.

---

# 8. Case 1 — Same Name + Extension + Date + Size + Hash

Example:

```text
Folder_A/IMG_1234.JPG
Size: 4,523,112 bytes
SHA-256: ABC123...

Folder_B/IMG_1234.JPG
Size: 4,523,112 bytes
SHA-256: ABC123...
```

These are exact duplicates.

### Action

Keep one representative.

Copy only the selected representative to:

```text
Images/
```

Do not copy the other duplicate into the final image collection.

The original duplicate remains untouched in the source directory.

---

# 9. Case 2 — Same Name + Extension but Different Content

Example:

```text
Folder_A/IMG_1234.JPG
Size: 2 MB
SHA-256: ABC123

Folder_B/IMG_1234.JPG
Size: 5 MB
SHA-256: XYZ789
```

The filenames are identical but the contents are different.

### Action

**Keep both.**

Both images are copied to the output collection.

Filename alone must never be used to determine duplication.

---

# 10. Case 3 — Same Content but Different Filename

Example:

```text
IMG_1234.JPG
IMG_1234_copy.JPG
Vacation.jpg
```

All three have:

```text
SHA-256 = ABC123
```

They are byte-for-byte identical.

### Action

Keep one representative.

The original files remain untouched.

---

# 11. Case 4 — Same Content but Different Filesystem Date

Example:

```text
IMG_1234.JPG
Created: 2025-08-01

IMG_1234_copy.JPG
Created: 2025-09-15
```

If the SHA-256 hash is identical, the files contain the same bytes.

Different Windows filesystem timestamps do not make them different images.

### Action

Keep one representative.

---

# 12. Case 5 — Same Content but Different Extension

Example:

```text
image.jpg
image.jpeg
```

If both files have the same SHA-256 hash, they are exact duplicates.

### Action

Keep one representative.

The extension is not the primary identity of the file; its content is.

---

# 13. Case 6 — Same Filename and Same Size but Different Hash

Example:

```text
Folder_A/IMG_5555.JPG
Size: 3.2 MB
Hash: ABC

Folder_B/IMG_5555.JPG
Size: 3.2 MB
Hash: XYZ
```

These are different files.

### Action

Keep both.

---

# 14. Case 7 — Different File but Same Visual Image

Example:

```text
IMG_1234.JPG
4000 × 3000
5 MB

IMG_1234_resized.JPG
2000 × 1500
1.5 MB
```

The files have different binary contents and therefore different SHA-256 hashes.

However, they may represent the same photograph.

### Action

Classify as:

```text
NEAR_DUPLICATE
```

Do not automatically delete either version.

Place the relevant files in:

```text
Review\Near_Duplicates
```

This protects against accidental loss of higher-quality or edited versions.

---

# 15. Case 8 — Recompressed Image

Example:

```text
Original:
4000 × 3000
5.4 MB

Copy:
4000 × 3000
2.1 MB
```

The images may look almost identical while having different binary contents.

### Action

Classify as a potential near-duplicate and send it for review.

---

# 16. Case 9 — Edited Image

Example:

```text
IMG_1234.JPG
Original photograph

IMG_1234_edited.JPG
Brightness/contrast/crop applied
```

These may be visually similar but are not necessarily duplicates.

### Action

Keep both by default.

Classify as:

```text
POSSIBLE_EDITED_VERSION
```

---

# 17. Case 10 — Screenshots

Screenshots are treated as independent images unless they are exact duplicates.

Do not automatically remove screenshots merely because they are visually similar.

---

# 18. Case 11 — Burst Photos

iPhones can produce multiple photographs that look almost identical.

Example:

```text
IMG_1001.JPG
IMG_1002.JPG
IMG_1003.JPG
IMG_1004.JPG
```

These should normally be retained.

The application should not automatically delete burst-like sequences based only on visual similarity.

---

# 19. Case 12 — Live Photos

Live Photos can contain related image/video components.

For example:

```text
IMG_1234.HEIC
IMG_1234.MOV
```

These should not be treated as ordinary duplicate images.

The application should preserve them unless an explicit Live Photo policy is configured.

---

# 20. SHA-256 Hashing

SHA-256 is the primary mechanism for exact duplicate detection.

Conceptually:

```text
File
  ↓
Read binary content
  ↓
SHA-256
  ↓
Unique content fingerprint
```

Example:

```text
IMG_1234.JPG
    ↓
SHA-256
    ↓
a8f4c1........92e7
```

If:

```text
SHA256(A) == SHA256(B)
```

the files are treated as exact duplicates.

---

# 21. Why Filename Is Not the Primary Identifier

Filenames can change during imports.

Examples:

```text
IMG_0001.JPG
IMG_0001 (1).JPG
IMG_0001 (2).JPG
IMG_0001_copy.JPG
```

These may all represent the same file.

Conversely:

```text
Folder_A/IMG_0001.JPG
Folder_B/IMG_0001.JPG
```

may represent completely different photographs.

Therefore:

> **Content hash takes precedence over filename.**

---

# 22. EXIF Metadata

When available, the application should extract useful metadata such as:

- Date taken
- Camera make
- Camera model
- Image width
- Image height
- Orientation
- GPS availability
- Software/editor
- Other useful EXIF fields

The most important date for photographs is normally:

```text
DateTimeOriginal
```

because it represents the image capture time.

---

# 23. Date Priority

When choosing the best representative, dates should be considered in the following order:

```text
1. EXIF DateTimeOriginal
2. EXIF DateTimeDigitized
3. Windows creation date
4. Windows modification date
```

Filesystem dates may represent when a file was copied rather than when the photograph was taken.

---

# 24. Selecting the Best Exact Duplicate

When multiple exact copies exist, the application selects one representative.

Recommended priority:

1. Valid image metadata
2. Valid EXIF capture information
3. Image dimensions
4. File size
5. Original-looking filename
6. Deterministic source path ordering

For exact SHA-256 duplicates, file size should normally be identical.

The selection must be deterministic so that repeated scans produce consistent results.

---

# 25. Important: Larger File Does Not Always Mean Better Image

For different files, file size alone must not determine quality.

Example:

```text
Photo A
4032 × 3024
3 MB

Photo B
4032 × 3024
8 MB
```

The 8 MB file is not automatically better.

Quality decisions should consider:

```text
Resolution
+
Image format
+
Compression
+
Metadata
+
File size
```

For exact duplicates, SHA-256 is the decisive factor.

For non-identical images, the application should use a review classification rather than aggressive automatic deletion.

---

# 26. Output Filename Collision Handling

Two different images may have the same filename.

Example:

```text
IMG_1234.JPG
IMG_1234.JPG
```

If their hashes are different, both must be retained.

The output may therefore contain:

```text
Images/
├── IMG_1234.JPG
└── IMG_1234__2.JPG
```

The original filename is preserved as much as possible.

Any generated suffix applies only to the new output copy.

The source filename is never changed.

---

# 27. Destination Collision Logic

Before copying a file:

```text
Does destination filename exist?
        │
        ├── No
        │    └── Copy
        │
        └── Yes
             │
             ├── Same hash
             │    └── Skip duplicate
             │
             └── Different hash
                  └── Generate safe filename
```

This prevents accidental overwriting.

---

# 28. Near-Duplicate Detection

The application may use perceptual hashing such as:

- pHash
- dHash
- aHash

These algorithms are fundamentally different from SHA-256.

### SHA-256

Detects:

```text
EXACT SAME FILE
```

### Perceptual hash

Can detect:

```text
VISUALLY SIMILAR IMAGE
```

For example:

```text
Original.jpg
    ↓
Resize
    ↓
Compress
    ↓
Save as New.jpg
```

SHA-256:

```text
Different
```

Perceptual similarity:

```text
Very similar
```

Near-duplicate detection should therefore be treated as a **review mechanism**, not an automatic deletion mechanism.

---

# 29. Recommended Classification System

Every image should ultimately receive a classification.

Possible classifications:

```text
UNIQUE
EXACT_DUPLICATE
SAME_NAME_DIFFERENT_CONTENT
NEAR_DUPLICATE
POSSIBLE_EDITED_VERSION
LIVE_PHOTO_COMPONENT
SCREENSHOT
BURST_CANDIDATE
REVIEW_REQUIRED
```

---

# 30. Recommended Actions

| Classification | Action |
|---|---|
| `UNIQUE` | Copy to `Images` |
| `EXACT_DUPLICATE` | Copy only selected representative |
| `SAME_NAME_DIFFERENT_CONTENT` | Copy both |
| `NEAR_DUPLICATE` | Copy to `Review` |
| `POSSIBLE_EDITED_VERSION` | Keep both / Review |
| `LIVE_PHOTO_COMPONENT` | Keep |
| `SCREENSHOT` | Keep |
| `BURST_CANDIDATE` | Keep |
| `REVIEW_REQUIRED` | Copy to `Review` |

The default philosophy is:

> **When uncertain, keep the file.**

---

# 31. Dry-Run Mode

The application should support a dry-run mode.

Example:

```bash
python organize_images.py --dry-run
```

Dry-run mode:

- Scans the source.
- Calculates hashes.
- Reads metadata.
- Performs duplicate analysis.
- Produces reports.
- Shows proposed actions.
- Does not copy files.

This allows the user to inspect the results before creating the final collection.

---

# 32. Normal Copy Mode

After reviewing the dry-run reports:

```bash
python organize_images.py
```

The application creates the output directory and copies the selected files.

The source remains untouched.

---

# 33. Verification

After copying, the application should verify that the destination file exists.

For stronger verification, the application should optionally compare:

```text
Source SHA-256
        ==
Destination SHA-256
```

Example:

```text
Source:
IMG_1234.JPG
SHA-256: ABC123

Destination:
Images/IMG_1234.JPG
SHA-256: ABC123

Status:
VERIFIED
```

This confirms that the copied file is byte-for-byte identical to the source.

---

# 34. Reports

The application should generate detailed CSV reports.

## `scan_report.csv`

Contains every discovered image:

```text
source_path
filename
extension
file_size
sha256
width
height
exif_date
created_date
modified_date
format
classification
```

---

## `duplicate_report.csv`

Contains exact duplicate groups:

```text
duplicate_group
sha256
selected_file
duplicate_file
reason
action
```

Example:

```text
DUP-000001
ABC123
Folder_A/IMG_1234.JPG
Folder_B/IMG_1234.JPG
Same SHA-256
COPY_SELECTED_ONLY
```

---

## `review_report.csv`

Contains ambiguous or near-duplicate cases:

```text
file_a
file_b
similarity
reason
recommendation
```

Example:

```text
IMG_1234.JPG
IMG_1234_resized.JPG
98.7%
Possible resized duplicate
REVIEW
```

---

# 35. Summary Report

A human-readable summary should be generated:

```text
====================================================
iPHONE IMAGE CONSOLIDATION REPORT
====================================================

Source:
D:\Data\Pictures\iphone

Output:
D:\Data\Pictures\iphone_cleaned_2026-08-23_123000

----------------------------------------------------
SCAN
----------------------------------------------------

Files scanned:                 18,742
Image files:                   18,421
Unsupported files:                321

----------------------------------------------------
DUPLICATES
----------------------------------------------------

Exact duplicate files:          3,421
Exact duplicate groups:         1,204

Near duplicate candidates:        276
Possible edited versions:         102

Same filename / different hash:   124

----------------------------------------------------
OUTPUT
----------------------------------------------------

Images copied:                 14,982
Review files copied:              378

----------------------------------------------------
SOURCE MODIFICATION
----------------------------------------------------

Files deleted:                     0
Files moved:                       0
Files renamed:                     0
Files modified:                    0

====================================================
SOURCE WAS NOT MODIFIED
====================================================
```

---

# 36. Source Safety Requirements

The implementation must enforce the following rules.

### Rule 1 — Source is read-only

The source directory must only be read.

### Rule 2 — Output must be separate

The output directory must not be the source directory.

### Rule 3 — No deletion

The application must not call file deletion operations against source files.

### Rule 4 — No move

The application must not move source files.

### Rule 5 — No source rename

The application must not rename source files.

### Rule 6 — No source modification

The application must not write to source files.

### Rule 7 — No source metadata modification

EXIF and filesystem metadata must remain unchanged.

### Rule 8 — No source overwrite

Existing source files must never be overwritten.

### Rule 9 — Fail safely

If the output path is inside the source directory, the application should stop rather than risk recursively processing its own output.

### Rule 10 — Copy verification

Copied files should optionally be hash-verified.

---

# 37. Idempotency

Each execution should ideally create a timestamped output directory.

Example:

```text
D:\Data\Pictures
├── iphone
├── iphone_cleaned_2026-08-23_120000
└── iphone_cleaned_2026-08-23_133000
```

The source remains the master collection.

Repeated executions do not alter previous output collections unless an explicit cleanup operation is implemented separately.

---

# 38. Recommended Project Structure

```text
iphone-image-organizer/
│
├── README.md
├── requirements.txt
├── organize_images.py
├── config.py
│
├── src/
│   ├── scanner.py
│   ├── hashing.py
│   ├── metadata.py
│   ├── duplicate_detector.py
│   ├── similarity.py
│   ├── selector.py
│   ├── copier.py
│   ├── reporter.py
│   └── verifier.py
│
├── reports/
│
└── tests/
    ├── test_hashing.py
    ├── test_duplicates.py
    ├── test_selector.py
    ├── test_copy_safety.py
    └── test_collision_handling.py
```

---

# 39. Suggested Dependencies

Depending on the implementation, the project may use libraries such as:

```text
Pillow
pillow-heif
ImageHash
pandas
tqdm
```

Potential responsibilities:

| Library | Purpose |
|---|---|
| Pillow | Image reading, dimensions and metadata |
| pillow-heif | HEIC/HEIF support |
| ImageHash | Perceptual hashing |
| pandas | CSV/report generation |
| tqdm | Progress indicators |

The exact dependencies should be finalized based on the implementation.

---

# 40. Example Execution

### Step 1 — Configure source

```text
SOURCE_DIR = D:\Data\Pictures\iphone
```

### Step 2 — Perform dry run

```bash
python organize_images.py --dry-run
```

### Step 3 — Review reports

Check:

```text
Reports/
├── scan_report.csv
├── duplicate_report.csv
├── review_report.csv
└── summary.txt
```

### Step 4 — Create consolidated copy

```bash
python organize_images.py
```

### Step 5 — Verify output

The program verifies the copied files and generates the final summary.

---

# 41. Example Final Result

Before processing:

```text
D:\Data\Pictures\iphone
│
├── Import_01
│   └── 5,000 images
│
├── Import_02
│   └── 7,000 images
│
└── Import_03
    └── 6,000 images
```

After processing:

```text
D:\Data\Pictures
│
├── iphone
│   ├── Import_01
│   ├── Import_02
│   └── Import_03
│
└── iphone_cleaned_2026-08-23_123000
    │
    ├── Images
    │   ├── IMG_0001.JPG
    │   ├── IMG_0002.HEIC
    │   ├── IMG_0003.JPG
    │   └── ...
    │
    ├── Review
    │   ├── Near_Duplicates
    │   └── Possible_Edits
    │
    └── Reports
        ├── scan_report.csv
        ├── duplicate_report.csv
        ├── review_report.csv
        └── summary.txt
```

---

# 42. Final Safety Guarantee

The most important expected outcome is:

```text
Original source files:
        UNTOUCHED

Original source folders:
        UNTOUCHED

Original filenames:
        UNTOUCHED

Original EXIF metadata:
        UNTOUCHED

Original filesystem metadata:
        UNTOUCHED

Files deleted:
        0

Files moved:
        0

Files renamed:
        0

New cleaned collection:
        CREATED BY COPYING ONLY
```

The original iPhone import remains available as the **source of truth**.

The newly created directory becomes the **cleaned working collection**.

---

# 43. Design Principle

The application should always prefer **data preservation over aggressive deduplication**.

The decision hierarchy is:

```text
                ┌─────────────────────┐
                │   Source Images     │
                │     READ ONLY       │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │      Scan Files     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Extract Metadata    │
                │ Calculate SHA-256   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Exact Duplicate?    │
                └──────┬────────┬─────┘
                       │        │
                     YES        NO
                       │        │
                       ▼        ▼
                Select Best    Continue
                Representative Analysis
                       │        │
                       │        ▼
                       │   Near Duplicate?
                       │        │
                       │   ┌────┴────┐
                       │  YES       NO
                       │   │         │
                       │   ▼         ▼
                       │ Review     Keep
                       │
                       └────┬───────┘
                            │
                            ▼
                     COPY TO OUTPUT
                            │
                            ▼
                      VERIFY COPY
                            │
                            ▼
                     GENERATE REPORT
```

---

## 44. Golden Rule

> **If the program is not 100% confident that two files are the same, it must preserve both.**

This rule is intentional.

The purpose of the project is not to aggressively reduce the number of files. The purpose is to create a **cleaner image collection while minimizing the risk of losing a genuine photograph**.

The original directory is always preserved, and the cleaned collection is created exclusively through copying.
