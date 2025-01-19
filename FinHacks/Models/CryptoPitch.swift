import Foundation

struct CryptoPitch: Identifiable {
    let id: UUID
    let user: User           // User who created the pitch
    let crypto: Crypto       // Crypto object for detailed data
    let thesis: String       // User's reasoning or pitch content
    let pitchPrice: Double   // Price of the crypto at the time of the pitch
    let returnPercentage: Double // Calculated return percentage since the pitch
    let likes: Int           // Number of likes
    let comments: [Comment]  // List of comments (using the Comment class)
    let shares: Int          // Number of shares
    let createdAt: Date      // Date and time when the pitch was created
}
