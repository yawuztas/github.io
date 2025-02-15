<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Collect form data
    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $message = htmlspecialchars($_POST['message']);

    // Email details
    $to = "yvztas@gmail.com";
    $subject = "Yeni İletişim Formu Mesajı";
    $body = "Ad: $name\nE-posta: $email\n\nMesaj:\n$message";
    $headers = "From: $email";

    // Send email
    if (mail($to, $subject, $body, $headers)) {
        echo "Mesajınız başarıyla gönderildi.";
    } else {
        echo "Mesaj gönderilirken bir hata oluştu.";
    }
} else {
    echo "Bu sayfa sadece POST isteklerini kabul eder.";
}
?>