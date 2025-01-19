import SwiftUI

struct CommentsListView: View {
    let comments: [Comment]

    var body: some View {
        ScrollView {
            VStack {
                ForEach(comments) { comment in
                    CommentView(comment: comment)
                        .padding(.horizontal)
                }
            }
        }
    }
}
