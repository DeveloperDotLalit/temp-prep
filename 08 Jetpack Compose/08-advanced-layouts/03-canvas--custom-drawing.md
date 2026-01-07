---
layout: default
title: Canvas & Custom Drawing
parent: 8. Advanced Layouts & Graphics
nav_order: 3
---

# Canvas & Custom Drawing

Here are your notes for **Topic 8.3**.

---

## **Topic 8.3: Canvas & Custom Drawing**

### **1. What It Is**

The `Canvas` composable gives you a blank rectangular area where you can draw 2D graphics manually.
Instead of composing UI widgets (like Buttons or Text), you are issuing low-level drawing commands: "Draw a red line from (0,0) to (100,100)" or "Fill a circle with blue."

### **2. Why It Exists (Visual Freedom)**

You need `Canvas` when:

- **Data Visualization:** You are building a Line Chart, Pie Chart, or Histogram.
- **Custom Decor:** You need a weird background shape (like a wave) that isn't a standard rectangle.
- **Photo Editing:** You are building a cropping tool or a drawing app.

### **3. How It Works (The DrawScope)**

The `Canvas` exposes a `DrawScope`. This scope provides:

1. **Coordinate System:** (0,0) is the **Top-Left**. x increases to the right, y increases downwards.
2. **Size:** `size.width` and `size.height` tell you how big your canvas is.
3. **Functions:** `drawLine`, `drawRect`, `drawCircle`, `drawPath`, `drawArc`.

### **4. Key Concepts**

#### **A. Brush (Gradients)**

You don't just draw with solid colors. A `Brush` allows you to paint with gradients.

- `Brush.horizontalGradient(colors)`
- `Brush.radialGradient(colors)`
- `Brush.sweepGradient(colors)`

#### **B. Path (Complex Shapes)**

For anything that isn't a simple circle or square, you use a `Path`.

- `moveTo(x, y)`: Lift pen and move to start.
- `lineTo(x, y)`: Draw a line to here.
- `quadraticBezierTo(x1, y1, x2, y2)`: Draw a curve.
- `close()`: Draw a line back to the start to seal the shape.

#### **C. Blend Modes**

Controls how new paint interacts with existing pixels (e.g., `BlendMode.SrcIn`, `BlendMode.Multiply`).

### **5. Example: Drawing a Speedometer (Arc + Gradient)**

```kotlin
@Composable
fun Speedometer() {
    Canvas(modifier = Modifier.size(200.dp)) {
        // 1. Define a Gradient Brush
        val gradient = Brush.sweepGradient(
            0.0f to Color.Red,
            0.5f to Color.Yellow,
            1.0f to Color.Green,
            center = center // Use the center of the canvas
        )

        // 2. Draw the Arc
        drawArc(
            brush = gradient,
            startAngle = 180f, // 9 o'clock
            sweepAngle = 180f, // Draw half circle (to 3 o'clock)
            useCenter = false, // Don't close the slice like a pie chart
            style = Stroke(width = 20.dp.toPx(), cap = StrokeCap.Round)
        )

        // 3. Draw a simplified needle
        drawLine(
            color = Color.Black,
            start = center,
            end = Offset(center.x, center.y - 80.dp.toPx()), // Pointing UP
            strokeWidth = 4.dp.toPx()
        )
    }
}

```

### **6. Interview Prep**

**Interview Keywords**
`DrawScope`, `Canvas`, Coordinate System (Top-Left origin), `Brush`, `Path`, `Stroke` vs `Fill`, `drawIntoCanvas` (Native Access), `nativeCanvas`.

**Interview Speak Paragraph**

> "For custom graphics like charts or unique background shapes, I use the `Canvas` composable. It exposes a `DrawScope` which provides access to drawing primitives like `drawPath`, `drawCircle`, and `drawArc`. Unlike XML drawables, this is programmatic, so I can animate properties easily. I often use `Brush` to create gradient effects rather than solid colors. If I need advanced native Android graphics features—like drawing text directly on the canvas (which DrawScope doesn't natively support easily)—I use `drawIntoCanvas` to access the underlying Android `nativeCanvas` object."

---

**Next Step:**
You can draw static shapes. Now, let's make them move.
Ready for **Topic 8.4: Graphics Layer & Modifiers**? This is the secret to high-performance animations (hardware acceleration).

---

## Navigation

â† Previous
Next â†’
