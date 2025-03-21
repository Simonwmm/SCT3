// Vulnerable Java code that should trigger CodeQL alerts

import java.sql.*;
import java.io.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;

@WebServlet("/user")
public class UserServlet extends HttpServlet {
    // 🚨 CodeQL: Potential SQL Injection (Unsafe string concatenation)
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String userId = request.getParameter("id"); // User-controlled input
        try {
            Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/testdb", "root", "password");
            Statement statement = connection.createStatement();
            String query = "SELECT * FROM users WHERE id = '" + userId + "'"; // Unsafe SQL query
            ResultSet resultSet = statement.executeQuery(query);
            while (resultSet.next()) {
                response.getWriter().println(resultSet.getString("username"));
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // 🚨 CodeQL: Potential Path Traversal (Unsafe file path construction)
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String fileName = request.getParameter("file"); // User-controlled input
        File file = new File("/uploads/" + fileName); // Unsafe file path
        if (file.exists()) {
            response.getWriter().println("File exists!");
        } else {
            response.getWriter().println("File does not exist!");
        }
    }
}