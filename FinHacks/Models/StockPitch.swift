import Foundation

struct StockPitch: Identifiable {
    let id: UUID
    let user: User
    let stock: Stock
    let thesis: String
    let pitchPrice: Double
    let returnPercentage: Double
    let likes: Int
    let comments: [Comment]    // List of comments as a separate class
    let shares: Int
    let createdAt: Date
}
