import AppKit
import AVFoundation
import CoreVideo
import Foundation

struct Slide {
    let title: String
    let subtitle: String
    let bullets: [String]
    let code: [String]
    let seconds: Int
}

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let outputDir = root.appendingPathComponent("campaigns/pinterest/standard-access-demo", isDirectory: true)
try FileManager.default.createDirectory(at: outputDir, withIntermediateDirectories: true)
let outputURL = outputDir.appendingPathComponent("soft-moon-studio-pinterest-api-demo.mov")
try? FileManager.default.removeItem(at: outputURL)

let slides = [
    Slide(
        title: "Soft Moon Studio Pinterest API Demo",
        subtitle: "Standard Access upgrade demonstration",
        bullets: [
            "The app is used by Soft Moon Studio to publish owned organic Pinterest content.",
            "Authentication uses Pinterest OAuth.",
            "No access tokens or client secrets are shown in this demo."
        ],
        code: [],
        seconds: 6
    ),
    Slide(
        title: "1. Pinterest OAuth Authentication",
        subtitle: "The user authorizes the app through Pinterest's OAuth screen.",
        bullets: [
            "Redirect URI: http://localhost:8080/callback",
            "Requested scopes: boards:read, pins:read, pins:write, user_accounts:read",
            "After approval, the app stores the access token locally in .env."
        ],
        code: [
            "$ python3 -u scripts/pinterest_oauth.py",
            "Opening Pinterest OAuth in your browser...",
            "OAuth token saved to .env",
            "Scopes: boards:read pins:read pins:write user_accounts:read"
        ],
        seconds: 9
    ),
    Slide(
        title: "2. Connected Business Account",
        subtitle: "The app verifies the authenticated Pinterest account.",
        bullets: [
            "Business name: Soft Moon Studio",
            "Username: TheSoftMoonStudio",
            "Account type: BUSINESS"
        ],
        code: [
            "$ python3 scripts/pinterest_api.py me",
            "{",
            "  \"business_name\": \"Soft Moon Studio\",",
            "  \"username\": \"TheSoftMoonStudio\",",
            "  \"account_type\": \"BUSINESS\"",
            "}"
        ],
        seconds: 8
    ),
    Slide(
        title: "3. Read Pinterest Boards",
        subtitle: "The app retrieves available boards so the user can choose where to publish.",
        bullets: [
            "The app only publishes to a board selected by the authenticated user.",
            "Example boards returned by the Pinterest API:"
        ],
        code: [
            "$ python3 scripts/pinterest_api.py boards",
            "404761153949992313  Calm Home Aesthetic",
            "404761153949992913  Cozy Lighting Ideas",
            "404761153949992267  Soft Living"
        ],
        seconds: 8
    ),
    Slide(
        title: "4. Create an Organic Pin",
        subtitle: "The app creates a Pin with board, title, description, link and image URL.",
        bullets: [
            "Pins are created only from Soft Moon Studio owned content.",
            "The destination URL points to softmoonstudio.com.",
            "The image URL is a public Soft Moon Studio asset."
        ],
        code: [
            "$ python3 scripts/pinterest_api.py create-pin --board \"Cozy Lighting Ideas\"",
            "{",
            "  \"title\": \"API Demo: Cozy Lighting Ideas\",",
            "  \"link\": \"https://softmoonstudio.com/...\",",
            "  \"media_source\": { \"source_type\": \"image_url\" }",
            "}"
        ],
        seconds: 9
    ),
    Slide(
        title: "Requested Standard Access",
        subtitle: "Purpose of the app",
        bullets: [
            "Publish Soft Moon Studio's own organic Pins to its authenticated business account.",
            "Use only the scopes required for board selection and Pin creation.",
            "Support consistent Pinterest publishing with correct titles, descriptions, links and boards."
        ],
        code: [],
        seconds: 6
    )
]

let width = 1920
let height = 1080
let fps: Int32 = 30

let writer = try AVAssetWriter(outputURL: outputURL, fileType: .mov)
let settings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: width,
    AVVideoHeightKey: height
]
let input = AVAssetWriterInput(mediaType: .video, outputSettings: settings)
input.expectsMediaDataInRealTime = false
let attrs: [String: Any] = [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
    kCVPixelBufferWidthKey as String: width,
    kCVPixelBufferHeightKey as String: height
]
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: attrs)
writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

func drawText(_ text: String, in rect: CGRect, size: CGFloat, weight: NSFont.Weight = .regular, color: NSColor = NSColor(calibratedWhite: 0.12, alpha: 1.0)) {
    let style = NSMutableParagraphStyle()
    style.lineSpacing = 8
    let attrs: [NSAttributedString.Key: Any] = [
        .font: NSFont.systemFont(ofSize: size, weight: weight),
        .foregroundColor: color,
        .paragraphStyle: style
    ]
    NSString(string: text).draw(in: rect, withAttributes: attrs)
}

func makeBuffer(slide: Slide) -> CVPixelBuffer {
    var buffer: CVPixelBuffer?
    CVPixelBufferCreate(kCFAllocatorDefault, width, height, kCVPixelFormatType_32ARGB, nil, &buffer)
    guard let pixelBuffer = buffer else { fatalError("Could not create pixel buffer") }
    CVPixelBufferLockBaseAddress(pixelBuffer, [])
    let context = CGContext(
        data: CVPixelBufferGetBaseAddress(pixelBuffer),
        width: width,
        height: height,
        bitsPerComponent: 8,
        bytesPerRow: CVPixelBufferGetBytesPerRow(pixelBuffer),
        space: CGColorSpaceCreateDeviceRGB(),
        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue
    )!

    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(cgContext: context, flipped: false)

    context.setFillColor(NSColor(calibratedRed: 0.965, green: 0.94, blue: 0.905, alpha: 1).cgColor)
    context.fill(CGRect(x: 0, y: 0, width: width, height: height))

    context.setFillColor(NSColor(calibratedRed: 0.98, green: 0.965, blue: 0.94, alpha: 1).cgColor)
    context.fill(CGRect(x: 110, y: 110, width: 1700, height: 860))

    context.setStrokeColor(NSColor(calibratedRed: 0.72, green: 0.64, blue: 0.55, alpha: 1).cgColor)
    context.setLineWidth(3)
    context.stroke(CGRect(x: 110, y: 110, width: 1700, height: 860))

    drawText(slide.title, in: CGRect(x: 170, y: 835, width: 1580, height: 90), size: 58, weight: .bold)
    drawText(slide.subtitle, in: CGRect(x: 170, y: 775, width: 1580, height: 55), size: 32, weight: .medium, color: NSColor(calibratedWhite: 0.32, alpha: 1))

    var y = 705
    for bullet in slide.bullets {
        drawText("• \(bullet)", in: CGRect(x: 200, y: y, width: 1500, height: 52), size: 30)
        y -= 62
    }

    if !slide.code.isEmpty {
        context.setFillColor(NSColor(calibratedWhite: 0.11, alpha: 1).cgColor)
        context.fill(CGRect(x: 180, y: 145, width: 1560, height: 340))
        var codeY = 415
        for line in slide.code {
            drawText(line, in: CGRect(x: 220, y: codeY, width: 1480, height: 34), size: 24, weight: .regular, color: NSColor(calibratedRed: 0.90, green: 0.86, blue: 0.78, alpha: 1))
            codeY -= 40
        }
    }

    drawText("Soft Moon Studio • Pinterest API demo", in: CGRect(x: 170, y: 65, width: 900, height: 40), size: 22, color: NSColor(calibratedWhite: 0.42, alpha: 1))

    NSGraphicsContext.restoreGraphicsState()
    CVPixelBufferUnlockBaseAddress(pixelBuffer, [])
    return pixelBuffer
}

var frame: Int64 = 0
for slide in slides {
    let buffer = makeBuffer(slide: slide)
    let frames = Int(fps) * slide.seconds
    for _ in 0..<frames {
        while !input.isReadyForMoreMediaData {
            Thread.sleep(forTimeInterval: 0.01)
        }
        adaptor.append(buffer, withPresentationTime: CMTime(value: frame, timescale: fps))
        frame += 1
    }
}

input.markAsFinished()
writer.finishWriting {
    print(outputURL.path)
    exit(writer.status == .completed ? 0 : 1)
}
RunLoop.main.run()
