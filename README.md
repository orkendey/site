# Өркендеу — Vercel + Supabase transfer

This package contains the exact published multi-page demo (38 LMS catalog entries, 50 HTML pages and local images), plus a safe, read-only Supabase catalog seed.

## Vercel

Import this directory as a new Git repository/project with Framework Preset **Other**. `vercel.json` selects `dist` as output. No build/install step is needed; HTML and assets are prebuilt. Keep the current production domain unchanged until the preview is verified. To regenerate after editing Python source, run `python3 build.py` and deploy the new `dist`.

## Supabase

Create or choose a dedicated website project. Run `supabase/20260925_website_courses.sql` in its SQL Editor. It creates only `website_courses`, seeds the 38 catalog records and permits public reads, with no browser writes. Course images and LMS URLs refer to existing public LMS resources.

The prebuilt site currently displays the same 38 courses from its bundled snapshot; it does not yet fetch this table. A dynamic CMS, lead storage and Bitrix24 submissions require a later integration and should not be represented as working. Course hours with contradictions remain unset until verified. Do not put a service-role key in the browser or repository.
