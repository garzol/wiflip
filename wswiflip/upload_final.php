<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

session_start();

$UPLOAD_PASSWORD = 'shootagain';
$message = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  $pw = (string)($_POST['password'] ?? '');

  // étape login
  if (!empty($pw) && !empty($_POST['do_login'])) {
    if (hash_equals($UPLOAD_PASSWORD, $pw)) {
      $_SESSION['upload_authed'] = 1;
      header('Location: ' . strtok($_SERVER["REQUEST_URI"], '?') );
      exit;
    }
    $message = 'Mot de passe incorrect';
  }

  // étape upload
  if (!empty($_SESSION['upload_authed']) && isset($_FILES['files'])) {
    $uploadDir = __DIR__ . '/uploads';
    if (!is_dir($uploadDir)) mkdir($uploadDir, 0775, true);

    $files = $_FILES['files'];
    $count = is_array($files['name']) ? count($files['name']) : 0;

    $messageParts = [];
    for ($i = 0; $i < $count; $i++) {
      $tmp = $files['tmp_name'][$i];
      if (!is_uploaded_file($tmp)) continue;

      $name = $files['name'][$i];
      $safeName = preg_replace('/[^A-Za-z0-9._-]/', '_', $name);
      $target = $uploadDir . '/' . uniqid('upload_', true) . '_' . $safeName;

      if (move_uploaded_file($tmp, $target)) {
        $messageParts[] = htmlspecialchars($name);
      }
    }
    $message = 'Upload terminé: ' . (count($messageParts) ? implode(', ', $messageParts) : 'aucun fichier');
  }
}

$authed = !empty($_SESSION['upload_authed']);
?>
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Upload</title></head>
<body>
  <h1>Upload fichiers</h1>

  <?php if ($message): ?>
    <p style="color: #b00;"><?= htmlspecialchars($message) ?></p>
  <?php endif; ?>

  <?php if (!$authed): ?>
    <h2>Mot de passe</h2>
    <form method="post">
      <input type="password" name="password" autofocus>
      <input type="hidden" name="do_login" value="1">
      <button type="submit">Continuer</button>
    </form>
  <?php else: ?>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="files" multiple>
      <button type="submit">Upload</button>
    </form>
  <?php endif; ?>
</body>
</html>
