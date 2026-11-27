# Maintainer: sabb4th <eliassabat2@gmail.com>
pkgname=omayt
pkgver=1.4.0
pkgrel=1
pkgdesc="Omarchy YouTube TUI with Sixel/Kitty HD thumbnails, Cava FFT, and VA-API"
arch=('any')
url="https://github.com/sabb4th/omayt"
license=('MIT')
depends=('python' 'fzf' 'yt-dlp' 'mpv' 'ffmpeg' 'libsixel')
optdepends=(
  'chafa: fallback terminal graphics renderer'
  'wl-clipboard: copy video URLs to Wayland clipboard'
  'libnotify: desktop notifications when copying links'
)
source=("$pkgname-$pkgver.tar.gz::https://github.com/sabb4th/omayt/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('ce52d51e522a885f0b32fbcafbc43fba1d7677bbd81e2693524157adeca64e6f')

package() {
  cd "$srcdir/$pkgname-$pkgver"
  install -Dm755 omayt "$pkgdir/usr/bin/omayt"
  install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
  install -Dm644 README.md "$pkgdir/usr/share/doc/$pkgname/README.md"
  install -Dm644 README.pt-BR.md "$pkgdir/usr/share/doc/$pkgname/README.pt-BR.md"
  install -Dm644 README.fr.md "$pkgdir/usr/share/doc/$pkgname/README.fr.md"
}
