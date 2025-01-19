import Foundation

struct Comment: Identifiable {
    let id: UUID                // Unique identifier for the comment
    let user: User              // The user who posted the comment
    let content: String         // Text content of the comment
    let createdAt: Date         // Timestamp for when the comment was made
    let likes: Int              // Number of likes on the comment
    let parentCommentID: UUID?  // If it's a reply, the ID of the parent comment
    let replies: [Comment]      // List of replies to this comment
}
