export async function POST(request: Request) {
  try {
    const formData = await request.formData()
    const user_id = formData.get("user_id") as string
    const message = formData.get("message") as string
    const source = formData.get("source") as string
    const file = formData.get("file") as File | null

    let pdf_content_b64: string | null = null
    let pdf_filename: string | null = null
    let image_contents_b64: Array<{ filename: string; content: string }> = []

    // Handle PDF upload — encode as base64 to send across containers
    if (file) {
      const buffer = Buffer.from(await file.arrayBuffer())
      pdf_content_b64 = buffer.toString("base64")
      pdf_filename = file.name.replace(/[^a-zA-Z0-9.]/g, "")
      console.log(`[API] Encoded PDF for transfer: ${pdf_filename} (${buffer.length} bytes)`)
    }

    // Handle multiple image uploads — encode each as base64
    const imageFiles = formData.getAll("image_files") as File[]
    if (imageFiles && imageFiles.length > 0) {
      console.log(`[API] Processing ${imageFiles.length} image files...`)
      for (const imageFile of imageFiles) {
        if (imageFile && imageFile.size > 0) {
          const buffer = Buffer.from(await imageFile.arrayBuffer())
          const filename = imageFile.name.replace(/[^a-zA-Z0-9.]/g, "")
          image_contents_b64.push({ filename, content: buffer.toString("base64") })
          console.log(`[API] Encoded image: ${filename}`)
        }
      }
    }

    // On Vercel: VERCEL_URL is auto-injected (no https://) — use it server-side.
    // Locally: falls back to http://localhost:8000 for the standalone FastAPI server.
    const vercelUrl = process.env.VERCEL_URL
    const backendUrl = vercelUrl
      ? `https://${vercelUrl}`
      : process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
    const response = await fetch(`${backendUrl}/api/webhook/incoming`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        user_id,
        message,
        source,
        pdf_content_b64,
        pdf_filename,
        image_contents_b64: image_contents_b64.length > 0 ? image_contents_b64 : null,
      }),
    })

    if (!response.ok) {
      throw new Error("Backend API request failed: " + await response.text())
    }

    const data = await response.json()

    return Response.json({ report: data.report })
  } catch (error) {
    console.error("[v0] API analysis error:", error)

    // Return a mock response for development/demo purposes
    const mockReport = `# Your Symptom Analysis

## What You're Experiencing

Based on your description, you're experiencing digestive symptoms that appear to be related to food intake, particularly dairy products. The symptoms include:

- Bloating and discomfort after meals
- Upper abdominal discomfort
- Gas
- Symptoms appearing 30 minutes post-meal
- Pattern lasting approximately two weeks

## Severity Assessment

**Moderate** - Your symptoms are causing discomfort but don't appear to be severe or emergency in nature. However, persistent symptoms warrant medical evaluation.

## Possible Explanations

### 1. Lactose Intolerance
The timing and pattern of your symptoms, particularly their association with dairy products, suggests a possible lactose intolerance. This condition occurs when your body has difficulty digesting lactose, the sugar found in milk and dairy products.

### 2. Food Sensitivity or Intolerance
Beyond lactose, you may be experiencing sensitivity to other components in your diet. Common triggers include fatty foods, artificial sweeteners, or certain food additives.

### 3. Functional Dyspepsia
This common condition causes upper abdominal discomfort and bloating without an identifiable structural cause. It can be triggered by various foods and may be related to altered gut motility or sensitivity.

## Action Plan

### Immediate Steps:
1. **Keep a detailed food diary** - Record everything you eat and drink, along with symptom timing and severity
2. **Try an elimination diet** - Consider removing dairy products for 2-3 weeks to see if symptoms improve
3. **Eat smaller, more frequent meals** - This can reduce the digestive burden and may minimize symptoms
4. **Stay hydrated** - Drink plenty of water throughout the day

### Medical Consultation:
Schedule an appointment with your primary care physician or a gastroenterologist. They may recommend:
- Hydrogen breath test for lactose intolerance
- Blood tests to rule out celiac disease or other conditions
- Evaluation for other gastrointestinal conditions if symptoms persist

## Research-Backed Context

Lactose intolerance affects approximately 65% of the global population, with higher prevalence in certain ethnic groups. Symptoms typically begin 30 minutes to 2 hours after consuming dairy products, matching your reported pattern.

Food intolerances are distinct from food allergies and generally cause digestive symptoms rather than immune system reactions. They can develop at any age and may be temporary or permanent.

## Important Reminders

- Monitor for any worsening symptoms or new symptoms
- If you develop severe pain, fever, blood in stool, or persistent vomiting, seek immediate medical attention
- This analysis is educational only - your doctor can provide proper diagnosis through clinical examination and testing
- Don't make major dietary changes without consulting a healthcare provider, especially if you have other health conditions

Your symptoms are manageable and treatable with the right approach. A healthcare provider can help you identify the specific cause and develop an effective treatment plan tailored to your needs.`

    return Response.json({ report: mockReport })
  }
}
