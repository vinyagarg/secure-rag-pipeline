'use client'

// Lightweight client-side text extraction for uploaded documents.
// - txt / md: read natively as text
// - pdf: parse with pdf.js and concatenate the text layer of every page

let pdfjsPromise: Promise<typeof import('pdfjs-dist')> | null = null

async function getPdfjs() {
  if (!pdfjsPromise) {
    pdfjsPromise = import('pdfjs-dist').then((pdfjs) => {
      // Run the parser on a worker loaded from the matching CDN build.
      pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`
      return pdfjs
    })
  }
  return pdfjsPromise
}

async function extractPdf(file: File): Promise<string> {
  const pdfjs = await getPdfjs()
  const data = await file.arrayBuffer()
  const doc = await pdfjs.getDocument({ data }).promise
  const parts: string[] = []
  for (let n = 1; n <= doc.numPages; n++) {
    const page = await doc.getPage(n)
    const content = await page.getTextContent()
    const text = content.items
      .map((item) => ('str' in item ? item.str : ''))
      .join(' ')
    parts.push(text)
  }
  await doc.destroy()
  return parts.join('\n\n')
}

/** Returns the extracted plain text for a supported file, or '' on failure. */
export async function extractText(file: File, ext: string): Promise<string> {
  try {
    if (ext === 'pdf') {
      return normalize(await extractPdf(file))
    }
    // txt / md and any other text-like format
    return normalize(await file.text())
  } catch (err) {
    console.log('[v0] extractText failed:', (err as Error).message)
    return ''
  }
}

function normalize(text: string): string {
  return text
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim()
}
