import Foundation

struct User: Identifiable {
    let id: UUID
    let username: String
    let name: String
    let profilePicture: String
    let bio: String
    let followers: [UUID]
    let following: [UUID]

    // Stock Metrics
    let stockKarma: Int           // Karma specific to stock-related activity
    let totalStockLikes: Int      // Total likes received on stock pitches
    let totalStockPitches: Int    // Total number of stock pitches created

    // Crypto Metrics
    let cryptoKarma: Int          // Karma specific to crypto-related activity
    let totalCryptoLikes: Int     // Total likes received on crypto pitches
    let totalCryptoPitches: Int   // Total number of crypto pitches created

    // Activity
    let stockPitches: [UUID]      // List of IDs of stock pitches created by the user
    let likedStockPitches: [UUID] // List of IDs of stock pitches the user has liked
    let cryptoPitches: [UUID]     // List of IDs of crypto pitches created by the user
    let likedCryptoPitches: [UUID] // List of IDs of crypto pitches the user has liked
}
