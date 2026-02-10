//
//  MessageInputBar.swift
//  ui
//
//  Created by Sahana Rajashekara on 2/9/26.
//

import SwiftUI

struct MessageInputBar: View {
    @Binding var text: String
    var onSend: () -> Void
    
    var body: some View {
        HStack(spacing: 12) {
            TextField("Message...", text: $text)
                .padding(12)
                .background(Color.gray.opacity(0.1))
                .cornerRadius(20)
            
            Button(action: onSend) {
                Image(systemName: "arrow.up.circle.fill")
                    .font(.system(size: 32))
                    .foregroundColor(text.isEmpty ? .gray : .blue)
            }
            .disabled(text.isEmpty)
        }
        .padding()
    }
}

#Preview {
    MessageInputBar(text: .constant("Hello"), onSend: {})
}
